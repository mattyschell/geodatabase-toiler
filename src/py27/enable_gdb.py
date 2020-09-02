"""Enable gdb from ArcGIS (python 27)
"""
import os

import gdb

# C:\matt_projects\geodatabase-toiler>set SDEFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\mschell.sde
# C:\matt_projects\geodatabase-toiler>set AUTHFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\keycodes
# no arcpy2path environmental, we are already being called from the oldskool py27 

authfile = os.environ['AUTHFILE']

baby27gdb = gdb.Gdb()
baby27gdb.enable(authfile)
