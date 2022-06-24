# The ESRI Enterprise Geodatabase Administration Toilin'

Code and helpers for managing ESRI Enterprise Geodatabases.  It is our toil
friends, our rules, the trick is never to be afraid.

Pro first:
https://pro.arcgis.com/en/pro-app/help/data/geodatabases/manage-oracle/overview-geodatabases-oracle.htm

Oldskool:
https://desktop.arcgis.com/en/arcmap/10.7/manage-data/gdbs-in-oracle/overview-geodatabases-oracle.htm

## Requirements

1. ArcGIS Pro installed (ie Python 3+)
2. Database connectivity from this machine (ex 64 bit 19c Oracle client)
3. An .sde file that connects to the geodatabase (externalize as %SDEFILE%)


## Regression Test Code Written For The Toilin'

To guarantee all tests run execute as the "SDE" geodatabase administrator in a dev environment. 

```bat
> set SDEFILE=C:\XXX\Connections\xxx\env\xxx-xxxxxx\yyy.sde
> testall.bat
```

## Enable An Enterprise Geodatabase

A big bloated wrapper to arcpy.EnableEnterpriseGeodatabase_management. 

```bat
> set SDEFILE=C:\XXX\Connections\xxx\env\xxx-xxxxxx\yyy.sde
> set AUTHFILE=C:\XXX\Connections\xxx\env\xxx-xxxxxx\keycodes
> set ARCPY2PATH=C:\Python27\ArcGIS10.7
> enablegdb.bat
```

1. Checks required privileges
2. Spools SQL to a table so we can snoop on ESRI and debug errors
3. Shells out to ArcMap's python 2.7 for geodatabase creation.  Allows control over the version (ex 10.7.1)
4. Updates database keywords so we will default to native database geometries instead of ESRI ransomware 


