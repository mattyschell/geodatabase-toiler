CREATE OR REPLACE
TRIGGER db_ev_rename_st_metadata AFTER RENAME ON
DATABASE
DECLARE
    sql_text ora_name_list_t;

sql_elements BINARY_INTEGER;

rename_stmt VARCHAR2(2000) DEFAULT NULL;

pos NUMBER;

st_str NVARCHAR2(32);
BEGIN
IF
        (ora_sysevent = 'RENAME'
        AND (ora_dict_obj_type = 'TABLE'
        OR ora_dict_obj_type = 'VIEW')) THEN sql_elements := ora_sql_txt(sql_text);

FOR i IN 1.. sql_elements
LOOP
    rename_stmt := rename_stmt || REPLACE(sql_text(i), chr(0), '');
END
LOOP;

rename_stmt := UPPER(rename_stmt);

pos := INSTR(rename_stmt, ' TO ') + 4;

st_str := SUBSTR(rename_stmt, pos);

pos := 1;

WHILE pos > 0
LOOP
    pos := INSTR(st_str, ' ');
IF
    pos > 0 THEN st_str := SUBSTR(st_str, 1, pos - 1) || SUBSTR(st_str, pos + 1);
END
IF;
END
LOOP;

UPDATE
    sde.st_geometry_index
SET
    table_name = NULL
WHERE
    owner = ora_dict_obj_owner
    AND table_name = ora_dict_obj_name;

UPDATE
    sde.st_geometry_columns
SET
    table_name = st_str
WHERE
    owner = ora_dict_obj_owner
    AND table_name = ora_dict_obj_name;

UPDATE
    sde.st_geometry_index
SET
    table_name = st_str
WHERE
    owner = ora_dict_obj_owner
    AND table_name IS NULL;
END
IF;
END;
