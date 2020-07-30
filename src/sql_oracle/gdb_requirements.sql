DECLARE
    psql                varchar2(4000);
    dict_views          pls_integer := 0;    
    module_installed    pls_integer := 0;
    error_report        varchar2(4000) := '';
BEGIN
    BEGIN
        psql := 'select count(*) '
             || 'from '
             || '    dba_registry '
             || 'where '
             || '    rownum = 1';
        EXECUTE IMMEDIATE psql INTO dict_views;
    EXCEPTION
    WHEN OTHERS
    THEN
        dict_views := 0;
    END;

    -- Oracle Locator is a subset of functions within Oracle Spatial

    IF dict_views = 1
    THEN

        psql := 'select count(*) '
            || 'from '
            || '    dba_registry '
            || 'where '
            || '    comp_id = :p1 '
            || 'and UPPER(comp_name) LIKE :p2 ';
    
        EXECUTE IMMEDIATE psql INTO module_installed USING 'SDO'
                                                          ,'%SPATIAL%';

    ELSE

        psql := 'select count(*) '
             || 'from '
             || '    all_users '
             || 'where '
             || '    username = :p1 ';

        EXECUTE IMMEDIATE psql INTO module_installed USING 'MDSYS';

    END IF;

    IF module_installed = 0
    THEN

        error_report := error_report || CHR(10) || '| ORACLE LOCATOR IS NOT INSTALLED |' || CHR(10);

    END IF;

    -- ESRI enterprise geodatabase requires Oracle Text 

    IF dict_views = 1
    THEN

        EXECUTE IMMEDIATE psql INTO module_installed USING 'CONTEXT'
                                                          ,'%ORACLE TEXT%';

    ELSE

        EXECUTE IMMEDIATE psql INTO module_installed USING 'CTXSYS';

    END IF;

    IF module_installed = 0
    THEN

        error_report := error_report || CHR(10) || '| ORACLE TEXT IS NOT INSTALLED |' || CHR(10);

    END IF;

    IF LENGTH(error_report) > 0
    THEN

        RAISE_APPLICATION_ERROR(-20001,error_report);

    END IF;

END;
