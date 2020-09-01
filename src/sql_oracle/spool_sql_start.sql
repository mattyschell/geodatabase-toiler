declare
   psql varchar2(4000);
begin
    psql := 'drop table spoolsdesqlstart';
    begin
        execute immediate psql;
    exception when others then null;
    end;
    psql := 'drop table spoolsdesql';
    begin
        execute immediate psql;
    exception when others then null;
    end;
    psql := 'create table spoolsdesqlstart as '
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
         || 'from v$sql ';
    execute immediate psql;
end;