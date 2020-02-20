# The ESRI Enterprise Geodatabase Administration Toilin'

Code and helpers for ESRI Enterprise Geodatabases on Oracle 19c.


## Requirements

1. ArcGIS Pro installed (ie Python 3+)
2. Oracle 19c connectivity from this machine (ie 64 bit Oracle client)
3. An .sde file that connects to the database (externalize as %SDEFILE%)


## Test Repo Code Written For The Toilin'

```shell
> set SDEFILE=T:\GIS\Internal\Connections\oracle19c\ditgsdv1\mschell_ditgsdv1.sde
> testall.bat
```

## Test A Geodatabase And Report Areas Of Toil

```shell
> set SDEFILE=T:\GIS\Internal\Connections\oracle19c\ditgsdv1\mschell_ditgsdv1.sde
> testgdb.bat
```
