REM copy to \geodatabase-scripts
REM rename gdbeat-databasename
REM change these 
set DBENV=DEV
set DBNAME=XXXXXDVX
set DBTYPE=oracle19c
SET BASEPATH=X:\XXX
SET PROJECT=XXX 
REM unmask these
set NOTIFY=xxxx@xxxx.xxxx.xxx
set MAINTAINER=xxxx@xxxx.xxxx.xxx
set NOTIFYFROM=xxxxxx@xxxx.xxx.xxx
set SMTPFROM=xxxxxxxxx.xxxxxx
REM review the rest 
set SDEFILE=%BASEPATH%\connections\%DBTYPE%\%DBENV%\%PROJECT%-%DBNAME%\xxxxxxxxxxxxxxxx\sde.sde
set TOILER=%BASEPATH%\geodatabase-toiler\
set LOG=%BASEPATH%\geodatabase-scripts\logs\gdbeat\gdbeat_%DBNAME%.log
set SPAMSUCCESS=N
echo calling gdbeat on %date% at %time% > %LOG%
c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat %TOILER%src\py\gdbeat.py %SPAMSUCCESS% %NOTIFY% %DBTYPE% %DBNAME% %MAINTAINER%