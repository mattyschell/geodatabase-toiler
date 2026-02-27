set BASEPATH=X:\xxx
set SDEFILE=%BASEPATH%\xxx\xxx.sde
set PYTHON1=C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set PYTHON2=C:\Users\%USERNAME%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
if exist "%PYTHON1%" (
    set PROPY=%PYTHON1%
) else if exist "%PYTHON2%" (
    set PROPY=%PYTHON2%
)
call %PROPY% .\src\py\test_cx_sde.py 
call %PROPY% .\src\py\test_gdb.py
call %PROPY% .\src\py\test_fc.py
call %PROPY% .\src\py\test_version.py