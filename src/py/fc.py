import arcpy
import gdb

class fc(object):

    def __init__(self
                ,gdb 
                ,name
                ,database='oracle'):

        # gdb object
        self.gdb = gdb
        # ex BUILDING
        self.name = name.upper()
        self.database = database
        # esri tools frequently expect this C:/sdefiles/bldg.sde/BUILDING
        self.featureclass = gdb.sdeconn + "/" + self.name

    def exists(self):

        return arcpy.Exists(self.featureclass)

    def delete(self):

        arcpy.Delete_management(self.featureclass)

    def locksexist(self):

        if arcpy.TestSchemaLock(self.featureclass):

            # "True A schema lock can be applied to the dataset"
            return False

        else:

            return True

    def version(self);

        arcpy.RegisterAsVersioned_management(self.featureclass
                                            ,"NO_EDITS_TO_BASE")

    
        

