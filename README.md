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

To maximize test coverage execute as the geodatabase administrator ("sde") in a development environment. Copy sample-testall.bat to testall.bat and update the inputs.

```bat
> set SDEFILE=C:\XXX\Connections\xxx\env\xxx-xxxxxx\yyy.sde
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


