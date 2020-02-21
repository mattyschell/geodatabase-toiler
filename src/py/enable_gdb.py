"""Check for all prerequisites, and if met, enable enterprise gdb
"""
import arcpy
import os
import pathlib

import cx_sde
import gdb

def main():

    authfile = os.environ['AUTHFILE']
    sdeconn  = os.environ['SDEFILE']
    
    babygdb = gdb.Gdb()

    if  babygdb.checkconnection() \
    and babygdb.checkgdbadminprivs() \
    and babygdb.checkmodules() \
    and babygdb.checkgdbcreationprivs():
        
        # untested
        # need to look into return codes and errors and TEMP logs

        try:
            arcpy.EnableEnterpriseGeodatabase_management(sdeconn, 
                                                         authfile)
        
        except:

            print (arcpy.GetMessages())

main()     

    

        
