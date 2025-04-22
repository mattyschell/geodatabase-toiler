-- Test as SDE
create table foo
    (bar varchar2(4000));
create index 
    foobar 
on 
    foo(bar) INDEXTYPE IS CTXSYS.CONTEXT;
drop table foo;
--
-- If that fails
-- check for the default lexer on the pluggable database
-- this row should exist and
-- the pre_owner should be CTXSYS (not SYS)
--
-- SELECT * FROM CTXSYS.CTX_PREFERENCES
-- where pre_name = 'DEFAULT_LEXER'
--
-- PRE_OWNER  | PRE_NAME     |PRE_CLASS |PRE_OBJECT 
---------+-------------+---------+-----------
-- CTXSYS     |DEFAULT_LEXER |LEXER     |BASIC_LEXER
--
-- If no rows returned or owner is not CTXSYS
-- ask DBAs to set up Oracle text as "American" (lol) on the PDB
--
-- alter session set CURRENT_SCHEMA=CTXSYS;
-- @?/ctx/admin/defaults/dr0defin.sql "AMERICAN";
-- rerun the test above
