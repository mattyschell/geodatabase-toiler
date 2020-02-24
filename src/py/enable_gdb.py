"""Check for all prerequisites, and if met, enable enterprise gdb
"""
import os

import gdb

# C:\matt_projects\geodatabase-toiler>set SDEFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\mschell.sde
# C:\matt_projects\geodatabase-toiler>set AUTHFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\mschell_private\keycodes

authfile = os.environ['AUTHFILE']

babygdb = gdb.Gdb()
babygdb.enable(authfile)
