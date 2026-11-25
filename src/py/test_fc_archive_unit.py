import importlib.util
import pathlib
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest import mock
from zoneinfo import ZoneInfoNotFoundError


class ArchiveTestCase(unittest.TestCase):

    def setUp(self):
        self.arcpy = mock.Mock()
        self.arcpy.Exists.return_value = False
        self.arcpy.management.GetCount.return_value.getOutput.return_value = '1'
        self.arcpy.Describe.return_value = SimpleNamespace(
            isArchived=True, spatialReference='native projection')
        self.arcpy.EnvManager = mock.MagicMock()
        self.layer = self.arcpy.management.MakeFeatureLayer.return_value.getOutput.return_value
        spec = importlib.util.spec_from_file_location(
            'fc_archive_test_subject', pathlib.Path(__file__).with_name('fc.py'))
        module = importlib.util.module_from_spec(spec)
        with mock.patch.dict(sys.modules, {
                'arcpy': self.arcpy, 'gdb': mock.Mock(), 'cx_sde': mock.Mock()}):
            spec.loader.exec_module(module)
        self.module = module
        self.fc = module.Fc(
            SimpleNamespace(sdeconn=r'C:\connections\readonly.sde'),
            'bldg.building_historic')
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)

    def test_midnight_utc_converts_to_server_time_and_exports_native_data(self):
        for date, archive_date in (
                ('20260101', datetime(2025, 12, 31, 19)),
                ('20260701', datetime(2026, 6, 30, 20)),
                ('20240229', datetime(2024, 2, 28, 19))):
            with self.subTest(date=date):
                self.arcpy.reset_mock()
                output = self.fc.exportarchive(
                    date, self.tempdir.name)
                self.assertEqual(
                    pathlib.Path(output),
                    pathlib.Path(self.tempdir.name) /
                    'BUILDING_HISTORIC_{}.shp'.format(date))
                self.arcpy.management.ChangeVersion.assert_called_once_with(
                    self.layer, 'HISTORICAL', date=archive_date)
                self.arcpy.EnvManager.assert_called_once_with(
                    overwriteOutput=False,
                    outputCoordinateSystem='native projection', extent=None)
                self.arcpy.management.CopyFeatures.assert_called_once_with(
                    self.layer, output)
                self.arcpy.management.Delete.assert_called_once_with(self.layer)

    def test_invalid_dates_fail_before_accessing_data(self):
        for date in ('2026011', '20260230', '20260101extra',
                     '2026-01-01', '２０２６０１０１', None):
            with self.subTest(date=date):
                with self.assertRaises(ValueError):
                    self.fc.exportarchive(
                        date, self.tempdir.name, 'America/New_York')
        self.arcpy.Describe.assert_not_called()
        self.arcpy.management.MakeFeatureLayer.assert_not_called()

    def test_future_utc_date_is_rejected_before_accessing_data(self):
        with mock.patch.object(self.module, 'datetime', wraps=datetime) as clock:
            clock.now.return_value = datetime(
                2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
            with self.assertRaisesRegex(ValueError, 'future'):
                self.fc.exportarchive(
                    '20260101', self.tempdir.name, 'America/New_York')

        self.arcpy.Exists.assert_not_called()
        self.arcpy.Describe.assert_not_called()
        self.arcpy.ListFields.assert_not_called()
        self.arcpy.management.MakeFeatureLayer.assert_not_called()
        self.arcpy.management.CopyFeatures.assert_not_called()

    def test_current_utc_date_is_allowed_at_midnight(self):
        with mock.patch.object(self.module, 'datetime', wraps=datetime) as clock:
            clock.now.return_value = datetime(
                2026, 1, 1, tzinfo=timezone.utc)
            self.fc.exportarchive(
                '20260101', self.tempdir.name, 'America/New_York')

        self.arcpy.management.ChangeVersion.assert_called_once_with(
            self.layer, 'HISTORICAL', date=datetime(2025, 12, 31, 19))
        self.arcpy.management.CopyFeatures.assert_called_once()

    def test_excluded_fields_are_hidden_even_when_some_or_all_are_absent(self):
        excluded = (
            'last_edited_user', 'created_user', 'addressable', 'status',
            'condo_flags')
        retained = ('OBJECTID', 'SHAPE', 'BIN', 'LAST_EDITED_DATE',
                    'CREATED_DATE', 'LAST_STATUS_TYPE')
        source_fields = ('LAST_EDITED_USER', 'created_user', 'Addressable',
                         'STATUS', 'CONDO_FLAGS')
        for present in (source_fields, source_fields[:2], ()):
            with self.subTest(present=present):
                self.arcpy.reset_mock()
                self.arcpy.ListFields.return_value = [
                    SimpleNamespace(name=name) for name in retained + present]

                self.fc.exportarchive(
                    '20260101', self.tempdir.name, 'America/New_York',
                    exclude_fields=excluded)

                self.arcpy.ListFields.assert_called_once_with(self.fc.featureclass)
                self.assertEqual(
                    self.arcpy.FieldInfo.return_value.addField.call_args_list,
                    [mock.call(name, name, 'VISIBLE', 'NONE') for name in retained]
                    + [mock.call(name, name, 'HIDDEN', 'NONE') for name in present])
                self.assertIs(
                    self.arcpy.management.MakeFeatureLayer.call_args.kwargs['field_info'],
                    self.arcpy.FieldInfo.return_value)
                self.arcpy.management.CopyFeatures.assert_called_once()

    def test_missing_directory_and_existing_output_are_rejected(self):
        missing = pathlib.Path(self.tempdir.name) / 'missing'
        with self.assertRaises(NotADirectoryError):
            self.fc.exportarchive('20260101', str(missing), 'UTC')
        output = pathlib.Path(self.tempdir.name) / 'BUILDING_HISTORIC_20260101.shp'
        output.write_bytes(b'original')
        with self.assertRaises(FileExistsError):
            self.fc.exportarchive('20260101', self.tempdir.name, 'UTC')
        self.assertEqual(output.read_bytes(), b'original')
        self.arcpy.management.MakeFeatureLayer.assert_not_called()

    def test_unknown_archive_timezone_is_rejected(self):
        with self.assertRaises(ZoneInfoNotFoundError):
            self.fc.exportarchive(
                '20260101', self.tempdir.name, 'Not/A_Timezone')
        self.arcpy.management.MakeFeatureLayer.assert_not_called()

    def test_non_archived_source_is_rejected(self):
        self.arcpy.Describe.return_value.isArchived = False
        with self.assertRaisesRegex(ValueError, 'Archiving is not enabled'):
            self.fc.exportarchive('20260101', self.tempdir.name, 'UTC')
        self.arcpy.management.MakeFeatureLayer.assert_not_called()

    def test_empty_output_is_deleted_and_rejected(self):
        self.arcpy.management.GetCount.return_value.getOutput.return_value = '0'

        with self.assertRaisesRegex(ValueError, 'no rows; check archive start date'):
            self.fc.exportarchive(
                '20260101', self.tempdir.name, 'America/New_York')

        output = str(pathlib.Path(self.tempdir.name) /
                     'BUILDING_HISTORIC_20260101.shp')
        self.arcpy.management.CopyFeatures.assert_called_once_with(self.layer, output)
        self.arcpy.management.GetCount.assert_called_once_with(output)
        self.assertEqual(self.arcpy.management.Delete.call_args_list, [
            mock.call(output), mock.call(self.layer)])

    def test_historical_and_export_failures_propagate_and_release_layer(self):
        for operation in (self.arcpy.management.ChangeVersion,
                          self.arcpy.management.GetCount,
                          self.arcpy.management.CopyFeatures):
            with self.subTest(operation=operation):
                self.arcpy.reset_mock()
                error = RuntimeError('archive operation failed')
                operation.side_effect = error
                try:
                    with self.assertRaises(RuntimeError) as raised:
                        self.fc.exportarchive(
                            '20260101', self.tempdir.name, 'UTC')
                    self.assertIs(raised.exception, error)
                    self.arcpy.management.Delete.assert_called_once_with(self.layer)
                finally:
                    operation.side_effect = None


if __name__ == '__main__':
    unittest.main()
