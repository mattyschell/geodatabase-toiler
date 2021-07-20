-- sqlplus mschell/iluvesri247@primarydb @src/sql_oracle/helpers/dataguard_test.sql
DECLARE
    psql                VARCHAR2(4000);
    killswitch_minutes  pls_integer := 60; --lower for testing
BEGIN
    BEGIN
        psql := 'create table dg_test(site varchar2(50), times timestamp default systimestamp)';
        EXECUTE IMMEDIATE psql;
    EXCEPTION
    WHEN OTHERS THEN
        IF sqlcode = -955
        THEN
            psql := 'drop table dg_test';
            EXECUTE IMMEDIATE psql;
            psql := 'create table dg_test(site varchar2(50), times timestamp default systimestamp)';
            EXECUTE IMMEDIATE psql;
        ELSE 
            RAISE;
        END IF;
    END;
    
    FOR i IN 1 .. (killswitch_minutes * 60)
    LOOP
    
        psql := 'insert into dg_test values(:p1, :p2)';
        EXECUTE IMMEDIATE psql USING sys_context('USERENV','DB_UNIQUE_NAME')
                                    ,SYSDATE;
        COMMIT;
        DBMS_SESSION.SLEEP(.5);
    
    END LOOP;
    -- after getting kicked off of the primary
    -- check for matching records on both sides of data guard
    --
    -- SQL> select * from dg_test order by times desc;
    --
    -- SITE         |TIMES              
    -------------+-------------------
    -- ditcspd1_njdr|2021-07-20 11:50:39
    -- ditcspd1_njdr|2021-07-20 11:50:38
    -- ditcspd1_njdr|2021-07-20 11:50:38
    -- ditcspd1_njdr|2021-07-20 11:50:37

END;
/
