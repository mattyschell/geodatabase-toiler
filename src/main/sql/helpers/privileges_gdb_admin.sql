--data creator missing privileges
--https://pro.arcgis.com/en/pro-app/help/data/geodatabases/manage-oracle/privileges-oracle.htm
select regexp_substr('CREATE SEQUENCE,CREATE SESSION,CREATE TABLE,CREATE TRIGGER,CREATE VIEW,CREATE PROCEDURE','[^,]+', 1, level) 
    from dual
connect by regexp_substr('CREATE SEQUENCE,CREATE SESSION,CREATE TABLE,CREATE TRIGGER,CREATE VIEW,CREATE PROCEDURE', '[^,]+', 1, level) is not null
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