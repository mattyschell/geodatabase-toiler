import importlib.util
import pathlib
import sys
import unittest
from unittest import mock


class SDEContractTestCase(unittest.TestCase):

    def setUp(self):
        self.arcpy = mock.Mock(spec=['ArcSDESQLExecute', 'GetMessages'])
        self.connection = self.arcpy.ArcSDESQLExecute.return_value
        self.sde = r'C:\connections\test.sde'
        self.sql = 'SELECT value FROM example'

        # Load a private copy so discovery cannot replace integration tests' ArcPy.
        spec = importlib.util.spec_from_file_location(
            'cx_sde_unit_test_subject',
            pathlib.Path(__file__).with_name('cx_sde.py'),
        )
        self.cx_sde = importlib.util.module_from_spec(spec)
        with mock.patch.dict(sys.modules, {'arcpy': self.arcpy}):
            spec.loader.exec_module(self.cx_sde)

    def test_execute_immediate_preserves_raw_results(self):
        for result in (True, False, None, 'X', 1, 1.5, 1j, [], [[1], [None]]):
            with self.subTest(result=result):
                self.arcpy.reset_mock()
                self.connection.execute.return_value = result

                actual = self.cx_sde.execute_immediate(self.sde, self.sql)

                self.assertIs(actual, result)
                self.arcpy.ArcSDESQLExecute.assert_called_once_with(self.sde)
                self.connection.execute.assert_called_once_with(self.sql)
                self.connection.startTransaction.assert_not_called()
                self.connection.commitTransaction.assert_not_called()
                self.arcpy.GetMessages.assert_not_called()

    def test_execute_immediate_creates_a_connection_per_call(self):
        self.cx_sde.execute_immediate(self.sde, self.sql)
        self.cx_sde.execute_immediate(self.sde, self.sql)

        self.assertEqual(self.arcpy.ArcSDESQLExecute.call_args_list, [
            mock.call(self.sde),
            mock.call(self.sde),
        ])

    def test_connection_errors_preserve_cause_and_message(self):
        error = RuntimeError('connection failed')
        self.arcpy.ArcSDESQLExecute.side_effect = error

        for messages, expected in (
            ('ArcPy connection details', 'ArcPy connection details'),
            ('', str(error)),
        ):
            with self.subTest(messages=messages):
                self.arcpy.GetMessages.reset_mock()
                self.arcpy.GetMessages.return_value = messages

                with self.assertRaises(self.cx_sde.SDEConnectionError) as raised:
                    self.cx_sde.execute_immediate(self.sde, self.sql)

                self.assertIsInstance(raised.exception, RuntimeError)
                self.assertIs(raised.exception.__cause__, error)
                self.assertEqual(
                    str(raised.exception),
                    f"Failed to connect using SDE connection '{self.sde}': {expected}",
                )
                self.arcpy.GetMessages.assert_called_once_with()
                self.connection.execute.assert_not_called()

    def test_execution_errors_preserve_cause_and_message(self):
        error = RuntimeError('execution failed')
        self.connection.execute.side_effect = error

        for messages, expected in (
            ('ArcPy execution details', 'ArcPy execution details'),
            ('', str(error)),
        ):
            with self.subTest(messages=messages):
                self.arcpy.GetMessages.reset_mock()
                self.arcpy.GetMessages.return_value = messages

                with self.assertRaises(self.cx_sde.SDESQLExecutionError) as raised:
                    self.cx_sde.execute_immediate(self.sde, self.sql)

                self.assertIsInstance(raised.exception, RuntimeError)
                self.assertIs(raised.exception.__cause__, error)
                self.assertEqual(
                    str(raised.exception),
                    f'SQL execution failed for: {self.sql}\nArcPy message: {expected}',
                )
                self.arcpy.GetMessages.assert_called_once_with()

    def test_selectavalue_preserves_non_list_non_null_results(self):
        for result in (True, False, '', 'X', 0, 1, 1.5, 1j, (1,), {'value': 1}):
            with self.subTest(result=result):
                with mock.patch.object(
                    self.cx_sde, 'execute_immediate', return_value=result,
                ) as execute:
                    actual = self.cx_sde.selectavalue(self.sde, self.sql)

                self.assertIs(actual, result)
                execute.assert_called_once_with(self.sde, self.sql)

    def test_selectavalue_rejects_null(self):
        with mock.patch.object(self.cx_sde, 'execute_immediate', return_value=None):
            with self.assertRaises(ValueError) as raised:
                self.cx_sde.selectavalue(self.sde, self.sql)

        self.assertEqual(str(raised.exception), f'Returned NULL from {self.sql}')

    def test_selectavalue_rejects_all_lists(self):
        for result in ([], [1], [[1]], [[1], [2]]):
            with self.subTest(result=result):
                with mock.patch.object(
                    self.cx_sde, 'execute_immediate', return_value=result,
                ):
                    with self.assertRaises(ValueError) as raised:
                        self.cx_sde.selectavalue(self.sde, self.sql)

                self.assertEqual(
                    str(raised.exception),
                    f'Did not return single value on {self.sql}',
                )

    def test_selectacolumn_normalizes_results(self):
        cases = (
            (True, []),
            (False, [False]),
            ('', ['']),
            ('X', ['X']),
            (0, [0]),
            (1, [1]),
            (1.5, [1.5]),
            (1j, [1j]),
            (None, [None]),
            ([], []),
            ([[1]], [1]),
            ([[1], [None], [2]], [1, None, 2]),
            ([[1, 'ignored'], [2, 'also ignored']], [1, 2]),
        )
        for result, expected in cases:
            with self.subTest(result=result):
                with mock.patch.object(
                    self.cx_sde, 'execute_immediate', return_value=result,
                ) as execute:
                    actual = self.cx_sde.selectacolumn(self.sde, self.sql)

                self.assertIsInstance(actual, list)
                self.assertEqual(actual, expected)
                for value, expected_value in zip(actual, expected):
                    self.assertIs(type(value), type(expected_value))
                execute.assert_called_once_with(self.sde, self.sql)

    def test_selectacolumn_rejects_unsupported_types(self):
        for result in ((1,), {'value': 1}, b'X', object()):
            with self.subTest(result=result):
                with mock.patch.object(
                    self.cx_sde, 'execute_immediate', return_value=result,
                ):
                    with self.assertRaises(ValueError) as raised:
                        self.cx_sde.selectacolumn(self.sde, self.sql)

                self.assertEqual(
                    str(raised.exception),
                    f'Unknown return type from {self.sql}',
                )

    def test_selectacolumn_preserves_empty_row_error(self):
        with mock.patch.object(self.cx_sde, 'execute_immediate', return_value=[[]]):
            with self.assertRaises(IndexError):
                self.cx_sde.selectacolumn(self.sde, self.sql)

    def test_selection_helpers_propagate_execution_errors(self):
        for helper in (self.cx_sde.selectavalue, self.cx_sde.selectacolumn):
            for error_type in (
                self.cx_sde.SDEConnectionError,
                self.cx_sde.SDESQLExecutionError,
            ):
                with self.subTest(helper=helper.__name__, error=error_type.__name__):
                    error = error_type('failed')
                    with mock.patch.object(
                        self.cx_sde, 'execute_immediate', side_effect=error,
                    ):
                        with self.assertRaises(error_type) as raised:
                            helper(self.sde, self.sql)

                    self.assertIs(raised.exception, error)

    def test_execute_statements_uses_one_transaction_in_order(self):
        statements = ['INSERT first', 'INSERT second', 'INSERT third']

        result = self.cx_sde.execute_statements(self.sde, statements)

        self.assertIsNone(result)
        self.assertEqual(self.arcpy.mock_calls, [
            mock.call.ArcSDESQLExecute(self.sde),
            mock.call.ArcSDESQLExecute().startTransaction(),
            mock.call.ArcSDESQLExecute().execute(statements[0]),
            mock.call.ArcSDESQLExecute().execute(statements[1]),
            mock.call.ArcSDESQLExecute().execute(statements[2]),
            mock.call.ArcSDESQLExecute().commitTransaction(),
        ])

    def test_execute_statements_commits_an_empty_batch(self):
        result = self.cx_sde.execute_statements(self.sde, [])

        self.assertIsNone(result)
        self.assertEqual(self.connection.mock_calls, [
            mock.call.startTransaction(),
            mock.call.commitTransaction(),
        ])

    def test_execute_statements_accepts_an_iterator(self):
        statements = iter(['INSERT first', 'INSERT second'])

        self.cx_sde.execute_statements(self.sde, statements)

        self.assertEqual(self.connection.mock_calls, [
            mock.call.startTransaction(),
            mock.call.execute('INSERT first'),
            mock.call.execute('INSERT second'),
            mock.call.commitTransaction(),
        ])

    def test_execute_statements_ignores_false_results(self):
        self.connection.startTransaction.return_value = False
        self.connection.execute.return_value = False
        self.connection.commitTransaction.return_value = False

        result = self.cx_sde.execute_statements(self.sde, [self.sql])

        self.assertIsNone(result)
        self.assertEqual(self.connection.mock_calls, [
            mock.call.startTransaction(),
            mock.call.execute(self.sql),
            mock.call.commitTransaction(),
        ])

    def test_execute_statements_propagates_failures_without_explicit_rollback(self):
        statements = ['INSERT first', 'INSERT second', 'INSERT third']
        for stage in ('connect', 'start', 'execute', 'commit'):
            with self.subTest(stage=stage):
                self.arcpy.reset_mock(return_value=False, side_effect=True)
                self.connection.reset_mock(side_effect=True)
                error = RuntimeError(f'{stage} failed')
                expected_calls = [mock.call.ArcSDESQLExecute(self.sde)]
                if stage == 'connect':
                    self.arcpy.ArcSDESQLExecute.side_effect = error
                else:
                    expected_calls.append(mock.call.ArcSDESQLExecute().startTransaction())
                    if stage == 'start':
                        self.connection.startTransaction.side_effect = error
                    else:
                        expected_calls.extend([
                            mock.call.ArcSDESQLExecute().execute(statements[0]),
                            mock.call.ArcSDESQLExecute().execute(statements[1]),
                        ])
                        if stage == 'execute':
                            self.connection.execute.side_effect = [True, error]
                        else:
                            expected_calls.extend([
                                mock.call.ArcSDESQLExecute().execute(statements[2]),
                                mock.call.ArcSDESQLExecute().commitTransaction(),
                            ])
                            self.connection.commitTransaction.side_effect = error

                with self.assertRaises(RuntimeError) as raised:
                    self.cx_sde.execute_statements(self.sde, statements)

                self.assertIs(raised.exception, error)
                self.assertEqual(self.arcpy.mock_calls, expected_calls)


if __name__ == '__main__':
    unittest.main()
