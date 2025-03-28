## Set Up an ESRI Enterprise Geodatabase in Oracle 

We will be operating under this section of the ESRI documentation:

https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/manage-oracle/overview-geodatabases-oracle.htm

### Preparatory Steps

1. Upgrade to the latest ArcGIS Pro. This is ESRI's recommended best practice.
2. Track down a keycodes file.  This is required when enabling the enterprise geodatabase.


### Stabilization

1. Attend to the access control list. 
2. Request at least one login schema with at minimum "data creator" privileges
    * SQL to confirm: [..src/sql_oracle/privileges_data_creator.sql](https://github.com/mattyschell/geodatabase-toiler/blob/main/src/sql_oracle/privileges_data_creator.sql)
    * create a dummy table in this schema
3. Update all relevant tns_names files
4. Update runbook documentation
5. Verify that Oracle version is as expected
    * SELECT * FROM product_component_version;
6. Create or request creation of SDE user
    * docs: https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/manage-oracle/privileges-oracle.htm
    * DDL: [../src/sql_oracle/helpers/create_sde_ddl.sql](../src/sql_oracle/helpers/create_sde_ddl.sql)
7. Verify that oracle spatial and oracle text are installed
    * PL/SQL: [..src/sql_oracle/gdb_requirements.sql](../src/sql_oracle/gdb_requirements.sql) 
8. Verify that spatial_vector_acceleration is TRUE
    * select * from v$parameter where name like '%vector%'
9. Verify SDE privileges
    * SQL: [../src/sql_oracle/privileges_gdb_creation.sql](src/sql_oracle/privileges_gdb_creation.sql)
10. Run the enable enterise geodatabase tool from ArcGIS Pro
    * Docs: https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/enable-enterprise-geodatabase.htm
    * There is a python script in this repo. Don't use it.
11. Check for invalid objects
    * select * from user_objects where status <> 'VALID'
12. As SDE add a feature class to the database.  Review it. Delete it.
13. Check that the session count parameter is similar to other databases
    * SELECT name, value FROM v$parameter WHERE name = 'sessions';
14. Request application-specific database ROLEs
15. Request creation or import of application schemas
16. Grant roles to application schemas. 
17. Test roles. Change "rolename"
    * As schema1: create table rolenametest as select * from dual;
    * As schema1: grant select on rolenametest to "ROLENAME";
    * As schema2 with role: select * from schema1.rolenametest; 


### Post-Stabilization

1. Request installation of any utilities that the DBAs provide
2. Request the privileges to kill sessions if appropriate
3. Attend to the SDE DBTUNE table
4. Set up geodatabase heartbeat monitor

