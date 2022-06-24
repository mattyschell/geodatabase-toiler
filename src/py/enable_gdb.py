"""Check for all prerequisites, and if met, enable enterprise gdb
"""
import os
import logging

import gdb

# C:\matt_projects\geodatabase-toiler>set SDEFILE=XX:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\mschell.sde
# C:\matt_projects\geodatabase-toiler>set AUTHFILE=XX:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\keycodes
# C:\matt_projects\geodatabase-toiler>set ARCPY2PATH=C:\Python27\ArcGIS10.7
# C:\matt_projects\geodatabase-toiler\enablegdb.bat 
# calls this!

timestr = time.strftime("%Y%m%d-%H%M%S")
targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                        ,'enablegdb-{0}.log'.format(timestr))

logging.basicConfig(filename=targetlog
                   ,level=logging.INFO)
    
logging.info('Starting enable_gdb log')

authfile = os.environ['AUTHFILE']

# not SOP, we only need this for enablement 
arcpy2path = os.environ['ARCPY2PATH']

# initialize with optional py27 path
babygdb = gdb.Gdb(arcpy2path)

babygdb.spoolsql('start')

#enable using this keycodes file
try:
    babygdb.enable(authfile)
    exitcode = 0
except:
    exitcode = 1
finally:
    babygdb.spoolsql('stop')

logging.info('Completed enabling gdb, exit code is {0}'.format(exitcode))

exit(exitcode)