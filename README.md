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


## Test Repo Code Written For The Toilin'

To guarantee all tests run execute as the "SDE" geodatabase administrator in a 
dev environment.

```bat
> set SDEFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\SDE.sde
> testall.bat
```

## Enable An Enterprise Geodatabase

A big bloated wrapper to arcpy.EnableEnterpriseGeodatabase_management. 

```bat
> set SDEFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\mschell.sde
> set AUTHFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\keycodes
> enablegdb.bat
```

1. Checks required privileges
2. Shells out to ArcMap python 2.7 for geodatabase creation.  Allows us to control the version (ex 10.7.1)
3. Replaces keywords so we will use native database geometries instead of ESRI ransomware 

