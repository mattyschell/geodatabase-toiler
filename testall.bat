REM executes from ArcGIS Pro conda environment, SDEFILE env must be set
REM set SDEFILE=XX:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\bldg.sde
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_cx_sde.py 
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_gdb.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_fc.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_version.py
