declare
   psql varchar2(4000);
begin
    psql := 'create table spoolsdesql as '
         || 'select '
         || '   sql_text '
         || '  ,sql_fulltext '
         || '  ,sql_id '
         || '  ,first_load_time '
         || '  ,parsing_schema_name '
         || '  ,service '
         || '  ,module '
         || '  ,action '
         || '  ,last_load_time '
         || '  ,last_active_time '
         || 'from v$sql '
         || 'where sql_text not in '
         || '   (select sql_text from spoolsdesqlstart) ';
    execute immediate psql;
    psql := 'drop table spoolsdesqlstart';
    begin
        execute immediate psql;
    exception when others then null;
    end;
end;