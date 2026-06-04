import arcpy
import logging

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
            # elsewhere in ESRI methods we need only VERSIONNAME, 
            # it is annoying

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

        except Exception as exc:
            # Include ArcPy diagnostics, but keep noise low by trimming blanks and duplicates.
            gp_errors = (arcpy.GetMessages(2) or '').strip()
            gp_messages = (arcpy.GetMessages() or '').strip()

            details = []
            if gp_errors:
                details.append('arcpy errors: {0}'.format(gp_errors))
            if gp_messages and gp_messages != gp_errors:
                details.append('arcpy messages: {0}'.format(gp_messages))

            if len(details) == 0:
                details.append('arcpy returned no diagnostic messages')

            raise ValueError(
                "reconcileandpost of {0} totally bombed. {1}".format(self.versionname
                                                                      ,' | '.join(details))
            ) from exc
        
        output = resobject.getMessages()
        output_lower = output.lower()

        not_performed = [
            'was not performed',
            'no edit versions to reconcile',
        ]

        no_op_reconcile = any(msg in output_lower for msg in not_performed)

        if resobject.status != 4 \
        or 'warning' in output_lower  \
        or 'error' in output_lower \
        or no_op_reconcile:
            if no_op_reconcile:
                # ArcPy can report "Succeeded" for no-op reconciles; treat as operational failure.
                logging.info('reconcileandpost produced no-op output and is treated as failure for {0}'.format(self.versionname))
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

    def iseditable(self):

        # in our world editable is equivalent to public
        # since edits are performed by named user schemas

        # Lists the versions the connected user has permission to use
        #versions = arcpy.ListVersions(self.gdb.sdeconn)

        for version in arcpy.da.ListVersions(self.gdb.sdeconn):

            # print(version.name)
            # print(version.access)
            # SCHEMANAME.TEST_VERSION
            # Protected
            # https://pro.arcgis.com/en/pro-app/latest/arcpy/data-access/version.htm

            if  version.name == self.versionname \
            and version.access.upper() == 'PUBLIC':
                return True

        return False

    def protect(self):

        arcpy.management.AlterVersion(self.gdb.sdeconn
                                     ,self.name
                                     ,"" # name
                                     ,"" # description
                                     ,'PROTECTED')

    def unprotect(self):

        arcpy.management.AlterVersion(self.gdb.sdeconn
                                     ,self.name
                                     ,"" # name
                                     ,"" # description
                                     ,'PUBLIC')


