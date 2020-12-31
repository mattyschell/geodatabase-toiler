import arcpy

import gdb


class Version(object):

    def __init__(self
                ,gdb
                ,name
                ,parent='SDE.DEFAULT'):

        self.gdb = gdb
        self.name = name.upper()
        self.versionname = '{0}.{1}'.format(self.gdb.username.upper()
                                           ,self.name)
        self.parent = parent

    def exists(self):

        for version in arcpy.da.ListVersions(self.gdb.sdeconn):
            
            # List version returns 'SCHEMA.VERSIONNAME'
            # elsewhere in ESRI methods we need only VERSIONNAME, it is annoying

            if version.name == self.versionname:

                return True

        return False

    def delete(self):

        if self.exists():

            arcpy.DeleteVersion_management(self.gdb.sdeconn
                                          ,self.name)

    def create(self):

        if not self.exists():
        
            arcpy.CreateVersion_management(self.gdb.sdeconn
                                          ,self.parent
                                          ,self.name
                                          ,'PUBLIC')

    def reconcileandpost(self):

        # https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/reconcile-versions.htm
        # in our little universe it is always like so
        # we care hardly at all about automated reconcile
        # mostly postin
        
        try:
            resobject = arcpy.ReconcileVersions_management(self.gdb.sdeconn
                                                          ,'ALL_VERSIONS'
                                                          ,self.parent
                                                          ,self.versionname
                                                          ,'LOCK_ACQUIRED'
                                                          ,'ABORT_CONFLICTS'
                                                          ,'BY_OBJECT'
                                                          ,'FAVOR_EDIT_VERSION'
                                                          ,'POST'
                                                          ,'KEEP_VERSION'
                                                          ,None) #"c:\RecLog.txt")

        except: # Exception, inst:
            raise ValueError("reconcileandpost of {0} totally bombed".format(self.versionname))
        
        output = resobject.getMessages()

        if resobject.status != 4 \
        or 'warning' in output.lower()  \
        or 'error' in output.lower(): 
            raise ValueError("reconcileandpost of {0} failed, see {1}".format(self.versionname
                                                                             ,output))

        #Start Time: Wednesday, December 30, 2020 2:35:36 PM
        #Starting reconcile.
        #Reconciling version BLDG.TEST_VERSION with SDE.DEFAULT.
        #Posting version BLDG.TEST_VERSION to SDE.DEFAULT.
        #1 of 1 versions finished.
        #Finished reconcile.
        #Succeeded at Wednesday, December 30, 2020 2:35:41 PM (Elapsed Time: 4.93 seconds)
        return output
