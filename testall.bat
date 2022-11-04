REM executes from ArcGIS Pro conda environment, SDEFILE env must be set
set SDEFILE=X:\XXX\Connections\xxxxx\xxx\xxxx\xxx\xxx.sde
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_cx_sde_postgresql.py
set SDEFILE=X:\XXX\Connections\xxxxx\xxx\xxxx\xxx.sde
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_cx_sde.py 
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_gdb.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_fc.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_version.py
