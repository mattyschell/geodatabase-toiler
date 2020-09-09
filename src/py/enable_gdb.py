"""Check for all prerequisites, and if met, enable enterprise gdb
"""
import os

import gdb

# C:\matt_projects\geodatabase-toiler>set SDEFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\mschell.sde
# C:\matt_projects\geodatabase-toiler>set AUTHFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\keycodes
# C:\matt_projects\geodatabase-toiler>set ARCPY2PATH=C:\Python27\ArcGIS10.7
# C:\matt_projects\geodatabase-toiler\enablegdb.bat 
# calls this!

authfile = os.environ['AUTHFILE']

# not SOP, we only need this for enablement 
arcpy2path = os.environ['ARCPY2PATH']

# initialize with optional py27 path
babygdb = gdb.Gdb(arcpy2path)

babygdb.spoolsql('start')

#enable using this keycodes file
babygdb.enable(authfile)

babygdb.spoolsql('stop')
