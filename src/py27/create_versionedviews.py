"""Enable versioned views from ArcGIS (python 27)
"""
import os
import sys

# these are the skeleton 2.7 classes here in py27
import gdb
import fc

# C:\matt_projects\geodatabase-toiler>set SDEFILE=T:\GIS\Internal\Connections\oracle19c\dev\bldg.sde
# no arcpy2path environmental, we are already being called from the oldskool py27\python.exe

fcname = sys.argv[1]

gdb27 = gdb.Gdb()

fc27 = fc.Fc(gdb27
            ,fcname)

fc27.createversionedviews()


