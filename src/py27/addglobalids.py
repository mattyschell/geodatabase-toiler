import sys

# skeleton py27 classes
import gdb
import fc

# see building repo geodatabase-scripts/addglobalids.bat for a sample call
# keeping this sketchy: no tests, no logs, this is a monkey patch
# just one step up from right clicking in catalog

fcname = sys.argv[1]

gdb27 = gdb.Gdb()

fc27 = fc.Fc(gdb27
            ,fcname)

fc27.addglobalids()


