REM copy to \geodatabase-scripts
REM rename gdbeat-databasename
REM change these next three
set DBENV=DEV
set DBNAME=XXXXXDVX
set DBTYPE=oracle19c
SET BASEPATH=X:\XXX
REM unmask the next three
set NOTIFY=xxxx@xxxx.xxxx.xxx
set NOTIFYFROM=xxxxxx@xxxx.xxx.xxx
set SMTPFROM=xxxxxxxxx.xxxxxx
REM review the rest but should not need to change
set SDEFILE=%BASEPATH%\connections\%DBTYPE%\%DBENV%\GIS-%DBNAME%\xxxxxxxxxxxxxxxx\sde.sde
set TOILER=%BASEPATH%\geodatabase-toiler\
set LOG=%BASEPATH%\geodatabase-scripts\logs\gdbeat\gdbeat_%DATABASE%.log
set SPAMSUCCESS=N
echo calling gdbeat on %date% at %time% > %LOG%
c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat %TOILER%src\py\gdbeat.py %SPAMSUCCESS% %NOTIFY% %DBTYPE% %DBNAME%