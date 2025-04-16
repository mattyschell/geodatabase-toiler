REM executes from ArcGIS Pro conda environment
REM not sure why I was using conda B in the D
REM consider revising to standard python.exe
set BASEPATH=C:\xxx
set SDEFILE=%BASEPATH%\yyy\zzz.sde
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_cx_sde.py 
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_gdb.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_fc.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_version.py