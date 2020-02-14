--https://pro.arcgis.com/en/pro-app/help/data/geodatabases/manage-oracle/privileges-oracle.htm
select 
    'grant execute on SYS.' || table_name || ' to public;'
from 
    all_tab_privs
where 
    table_schema = 'SYS' 
and table_name IN ('DBMS_LOB','DBMS_LOCK','DBMS_PIPE','DBMS_UTILITY','DBMS_SQL','UTL_RAW')
and grantee = 'PUBLIC'
union all
select 'grant execute on SYS.' || table_name || ' to sde;' 
from all_tab_privs
where 
    table_schema = 'SYS' 
and table_name = 'DBMS_CRYPTO'
and grantee = 'SDE'
and privilege = 'EXECUTE'
union all
select regexp_substr('CREATE INDEXTYPE,CREATE LIBRARY,CREATE OPERATOR,CREATE PUBLIC SYNONYM,CREATE TYPE,CREATE VIEW,DROP PUBLIC SYNONYM,ADMINISTER DATABASE TRIGGER','[^,]+', 1, level) 
    from dual
connect by regexp_substr('CREATE INDEXTYPE,CREATE LIBRARY,CREATE OPERATOR,CREATE PUBLIC SYNONYM,CREATE TYPE,CREATE VIEW,DROP PUBLIC SYNONYM,ADMINISTER DATABASE TRIGGER', '[^,]+', 1, level) is not null
minus 
(
select privilege 
from 
    user_sys_privs
union
select r.privilege
from
    user_role_privs u
join
    role_sys_privs r
on 
    u.granted_role = r.role);
