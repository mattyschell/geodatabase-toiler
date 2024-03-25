REM executes from ArcGIS Pro conda environment, SDEFILE env must be set
set BASEPATH=C:\xx
set SDEFILE=%BASEPATH%\Connections\postgresql\env\server\database\xxxxx.sde
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_cx_sde_postgresql.py
set SDEFILE=%BASEPATH%\Connections\oracle19c\env\database\xxxxx.sde
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_cx_sde.py 
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_gdb.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_fc.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_version.py
