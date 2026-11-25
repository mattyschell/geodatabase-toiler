# The ESRI Enterprise Geodatabase Administration Toilin'

Code and helpers for managing ESRI Enterprise Geodatabases.  It is our toil friends, our rules, the trick is never to be afraid.

Pro first:
https://pro.arcgis.com/en/pro-app/help/data/geodatabases/manage-oracle/overview-geodatabases-oracle.htm

Oldskool:
https://desktop.arcgis.com/en/arcmap/10.7/manage-data/gdbs-in-oracle/overview-geodatabases-oracle.htm

## Requirements

1. ArcGIS Pro installed (ie Python 3+)
2. Database connectivity from this machine (ex 64 bit 19c Oracle client)
3. An .sde file that connects to the geodatabase (externalize as %SDEFILE%)


## Regression Test Code Written For The Toilin'

The database integration tests require the ArcGIS Pro environment and an SDE connection. To maximize test coverage execute as the geodatabase administrator ("sde") in a development environment. Copy sample-testall.bat to testall.bat and update the inputs.

```bat
> testall.bat
```

## Simple Wrappers For Simple People

The code in this repo is mostly simple opinionated wrappers to arcpy geodatabase, feature class, and versioning functions.

For example, import a feature class from another geodatabase and enable versioning.

```py
import gdb
import fc

targetfcname = 'TEST_TAXLOTS'
sourcefc     = """C:/connections/prod.sde/TAXLOTS"""

# SET SDEFILE=C:\connections\dev.sde
targetgdb = gdb.Gdb()

targetgdb.importfeatureclass(sourcefc
                            ,targetfcname)

targetfc = fc.Fc(targetgdb
                ,targetfcname)          

targetfc.version()                    
```

See /src/py/test_*.py for more usage demonstrations.

## Export a Historical Snapshot

For an archive-enabled feature class, export the archived DEFAULT version at
midnight UTC on a YYYYMMDD date:

```py
sourcefc = fc.Fc(gdb.Gdb()
                ,'BLDG.BUILDING_HISTORIC')
output = sourcefc.exportarchive('20260101'
                               ,r'C:\Temp')
```

Output is named BUILDING_HISTORIC_20260101.shp and existing output is rejected. Native attributes and projection are retained subject to shapefile format limitations

Pass an optional `exclude_fields` iterable to omit source fields before export,
for example `exclude_fields=('created_user', 'last_edited_user')`. Names are
matched case-insensitively and fields absent from the source are ignored.
Other callers retain all fields by default.
