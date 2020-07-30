select 'drop '  || owner || ' ' || type || ' ' ||  NAME ||';'
  FROM DBA_DEPENDENCIES 
 WHERE REFERENCED_OWNER = 'SDE'
 and owner = 'PUBLIC' 
 and type = 'SYNONYM'
union all
select 'drop '
       ||o.object_type
       ||' '||object_name
       ||case o.object_type when 'TABLE' then ' cascade constraints' when 'TYPE' then ' force' else '' end
       ||';'
from user_objects o
where o.object_type not in ('JOB','LOB','PACKAGE BODY','INDEX','TRIGGER')
and not exists (select 1
                from user_objects r
                where r.object_name = o.object_name 
                and   r.object_type = 'MATERIALIZED VIEW'
                and   o.object_type != 'MATERIALIZED VIEW'
               )