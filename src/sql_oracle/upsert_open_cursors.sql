-- https://pro.arcgis.com/en/pro-app/help/data/geodatabases/manage-oracle/update-open-cursors.htm
-- the sde.gdb_util.update_open_cursors expects SYSDBA access to run  dbms_utility.get_parameter_value
-- then loops over any user_schema geodatabases to spray the value into all server_config tables
-- we are simpletons here, just inserting the sql, gotta have select dictionary privs
-- From an older reference - Therefore, an ArcMap application with 10 layers being 
--                           edited in the document can potentially have 231 cursors open 
merge into server_config dest
using 
   (select upper(name) as prop_name
          ,NULL as char_prop_value
          ,value as num_prop_value 
    from v$parameter2 where name = 'open_cursors') src 
on (dest.prop_name=src.prop_name)
when not matched then 
   insert values(src.prop_name,src.char_prop_value, src.num_prop_value)
when matched 
   then update set dest.num_prop_value=src.num_prop_value
