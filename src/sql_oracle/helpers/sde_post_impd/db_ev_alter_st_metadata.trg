CREATE OR REPLACE
TRIGGER db_ev_alter_st_metadata AFTER ALTER ON
DATABASE
DECLARE
    TYPE stCols_T IS TABLE OF VARCHAR2(32);

st_cols stCols_T;

sql_text ora_name_list_t;

sql_elements BINARY_INTEGER;

rename_stmt VARCHAR2(2000);

pos NUMBER;

st_str VARCHAR2(32);

CURSOR st_table_cols (owner_wanted VARCHAR,
table_wanted VARCHAR) IS
SELECT
    column_name
FROM
    sde.st_geometry_columns
WHERE
    owner = owner_wanted
    AND table_name = table_wanted;
BEGIN
IF
        (ora_sysevent = 'ALTER'
        AND ora_dict_obj_type = 'TABLE') THEN OPEN st_table_cols (ora_dict_obj_owner,
        ora_dict_obj_name);

FETCH st_table_cols BULK COLLECT
INTO
    st_cols;

CLOSE st_table_cols;
IF
    st_cols.COUNT > 0 THEN FOR i IN st_cols.FIRST .. st_cols.LAST
LOOP
    IF
            ora_is_drop_column(st_cols(i)) = TRUE THEN
DELETE
FROM
    sde.st_geometry_columns
WHERE
    owner = ora_dict_obj_owner
    AND table_name = ora_dict_obj_name
    AND column_name = st_cols(i);
END
IF;
IF
    ora_is_alter_column(st_cols(i)) = TRUE THEN sql_elements := ora_sql_txt(sql_text);

FOR i IN 1.. sql_elements
LOOP
    rename_stmt := rename_stmt || UPPER(sql_text(i));
END
LOOP;

pos := INSTR(rename_stmt, 'TO') + 2;

st_str := SUBSTR(rename_stmt, pos);

pos := 1;

WHILE pos = 1
LOOP
    pos := INSTR(st_str, ' ');
IF
    pos = 1 THEN st_str := SUBSTR(st_str, 2);
END
IF;
END
LOOP;

pos := INSTR(st_str, ' ') - 1;
IF
    pos > 0 THEN st_str := SUBSTR(st_str, 1, pos);
END
IF;

UPDATE
    sde.st_geometry_index
SET
    table_name = NULL
WHERE
    owner = ora_dict_obj_owner
    AND table_name = ora_dict_obj_name;

UPDATE
    sde.st_partition_index
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

UPDATE
    sde.st_partition_index
SET
    table_name = st_str
WHERE
    owner = ora_dict_obj_owner
    AND table_name IS NULL;
END
IF;
END
LOOP;
END
IF;
END
IF;
END;