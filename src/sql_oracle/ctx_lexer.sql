-- Connect as CTXSYS inside the pluggable database, not at CDB level
-- This must be done from within the PDB context
ALTER SESSION SET CONTAINER = abcxyz;
-- user should be CTXSYS
EXEC CTX_DDL.CREATE_PREFERENCE('DEFAULT_LEXER', 'BASIC_LEXER');

-- test as SDE
-- SQL> show user
-- USER is "SDE"
-- SQL> create table foo (bar varchar2(4000));
-- Table created.
-- SQL> CREATE INDEX sample_index ON foo(bar) INDEXTYPE IS CTXSYS.CONTEXT;
-- 
-- SQL> drop table foo;
