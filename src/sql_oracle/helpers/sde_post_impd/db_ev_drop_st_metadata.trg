CREATE OR REPLACE
TRIGGER db_ev_drop_st_metadata AFTER DROP ON
DATABASE
BEGIN
IF
        (ora_dict_obj_type = 'TABLE') THEN
DELETE
FROM
    sde.st_geometry_columns
WHERE
    owner = ora_dict_obj_owner
    AND table_name = ora_dict_obj_name;
END
IF;
END;
