## Set Up an ESRI Enterprise Geodatabase in Oracle 

We will be operating under this section of the ESRI documentation:

https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/manage-oracle/overview-geodatabases-oracle.htm

### Preparatory Steps

1. Upgrade to the latest ArcGIS Pro. This is ESRI's recommended best practice.
2. Track down a "keycodes" file.  This is required when enabling the enterprise geodatabase. Keycode files seem to be immortal.


### Stabilization

1. Update all relevant tns_names files
2. Update runbook documentation
3. Attend to the access control list 
4. Create SDE schema
    * docs: https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/manage-oracle/privileges-oracle.htm
    * DDL: [../src/sql_oracle/helpers/create_sde_ddl.sql](../src/sql_oracle/helpers/create_sde_ddl.sql)
5. Verify that Oracle version is as expected
    * SELECT * FROM product_component_version;
6. Verify that oracle spatial and oracle text are installed
    * PL/SQL: [..src/sql_oracle/gdb_requirements.sql](../src/sql_oracle/gdb_requirements.sql) 
7. On a pluggable database: verify oracle text default lexer is set up 
    * verify from SDE ([..src/sql_oracle/ctx_lexer.sql](../src/sql_oracle/ctx_lexer.sql))
8. Verify that spatial_vector_acceleration is TRUE
    * select * from v$parameter where name like '%vector%'
9. Verify SDE privileges                
    * SQL: [..src/sql_oracle/privileges_gdb_creation.sql](../src/sql_oracle/privileges_gdb_creation.sql)
10. Run the EnableEnterpriseGeodatabase tool from ArcGIS Pro
    * Docs: https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/enable-enterprise-geodatabase.htm
11. Check for invalid objects
    * select * from user_objects where status <> 'VALID'
12. As SDE add a feature class to the database.  Review it. Delete it.
    * check geometry type and spatial reference
13. Update SDE open cursors
    * see [the docs](https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/manage-oracle/update-open-cursors.htm)
    * then ignore the docs and [..src/sql_oracle/sde_open_cursors.sql](../src/sql_oracle/sde_open_cursors.sql)
14. Check that the session count parameter is similar to other databases
    * SELECT name, value FROM v$parameter WHERE name = 'sessions';
    * Though take into consideration the high water mark on other databases
    * select resource_name, max_utilization from v$resource_limit where resource_name  'sessions';
15. Request any application-specific database roles
16. Request creation or import of application schemas
    * "data creator" privileges [see  docs](https://pro.arcgis.com/en/pro-app/help/data/geodatabases/manage-oracle/privileges-oracle.htm)
    * SQL to confirm: [..src/sql_oracle/privileges_data_creator.sql](../src/sql_oracle/privileges_data_creator.sql)
    * create a dummy table and/or feature class in these schemas
18. Grant any roles to these application schemas
19. Test roles. Change "rolename"
    * As schema1: create table rolenametest as select * from dual;
    * As schema1: grant select on rolenametest to "ROLENAME";
    * As schema2 with roles: select * from schema1.rolenametest; 
20. Request common system views in lieu of "select any dictionary"
    * View on dba_users


### Post-Stabilization

1. Request installation of any fancy utilities that the DBAs provide
2. Request the privileges to kill sessions if appropriate
3. Attend to the SDE DBTUNE table
4. Set up the geodatabase heartbeat monitor [..src/py/gdbeat.py](../src/py/gdbeat.py)

