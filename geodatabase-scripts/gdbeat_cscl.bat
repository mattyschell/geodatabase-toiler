REM change these next two
set DBENV=DEV
set DBNAME=XXXXXX
REM unmask the next three
set NOTIFY=xxxx@yyyy.zzzz.gov
set NOTIFYFROM=aaaa@bbbb.cccc.gov
set SMTPFROM=foo.bar
REM review the rest but should not need to change
set SDEFILE=C:\gis\connections\oracle19c\%DBENV%\CSCL-%DBNAME%\mschell_private\sde.sde
set TOILER=C:\gis\geodatabase-toiler\
set LOG=C:\gis\geodatabase-scripts\logs\gdbeat\gdbeat_%DATABASE%.log
set SPAMSUCCESS=N
echo calling gdbeat on %date% at %time% > %LOG%
c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat %TOILER%src\py\gdbeat.py %SPAMSUCCESS% %NOTIFY% 