-- https://desktop.arcgis.com/en/arcmap/10.7/manage-data/gdbs-in-oracle/privileges-oracle.htm
-- "Minimum privileges" are mostly available via the DB_APP_PROFILE
CREATE USER "SDE" IDENTIFIED BY iluvoracle247 DEFAULT TABLESPACE "SDE_DATA" TEMPORARY TABLESPACE "TEMP" PROFILE "DB_APP_PROFILE";
-- "You must grant the execute privilege on these packages to the public role to create or upgrade the geodatabase" 
GRANT EXECUTE ON dbms_pipe TO public;
GRANT EXECUTE ON dbms_lock TO public;
GRANT EXECUTE ON dbms_lob TO public;
GRANT EXECUTE ON dbms_utility TO public;
GRANT EXECUTE ON dbms_sql TO public;
GRANT EXECUTE ON utl_raw TO public;
-- "Privileges required for geodatabase creation or upgrade"
-- Again DB_APP_PROFILE covers most except...
GRANT CREATE VIEW TO "SDE";
GRANT EXECUTE ON DBMS_CRYPTO to "SDE";
GRANT CREATE INDEXTYPE to "SDE";
GRANT CREATE LIBRARY to "SDE";
GRANT CREATE OPERATOR to "SDE";
GRANT CREATE PUBLIC SYNONYM to "SDE";
GRANT DROP PUBLIC SYNONYM to "SDE";
GRANT EXECUTE ON DBMS_CRYPTO to "SDE";
GRANT ADMINISTER DATABASE TRIGGER to "SDE";
-- optional, carried over from 11g.  Used to debug issues with geodatabase-issued SQL
GRANT SELECT ANY DICTIONARY to "SDE";
--
-- verify, connect as SDE
-- @../privileges_gdb_creation.sql