CREATE or replace PROCEDURE ADD_BUILDING_CONSTR 
AS

        --mschell! 20200925

        psql                VARCHAR2(8000);
        addtable            varchar2(64);
    
BEGIN

    psql := 'select ''A'' || to_char(registration_id) '
            || 'from '
            || '    sde.table_registry '
            || 'where '
            || '    owner = :p1 '
            || 'and table_name = :p2 ';
    
    execute immediate psql into addtable using 'BLDG'
                                              ,'BUILDING';

    psql := 'ALTER TABLE ' || addtable || ' '
         || 'ADD CONSTRAINT ' || addtable || 'BIN '
         || 'CHECK '
         || '(bin >= 1000000 AND bin < 6000000)';

    EXECUTE IMMEDIATE psql;

END;