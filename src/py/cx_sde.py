import arcpy

class SDEConnectionError(RuntimeError):
    pass

class SDESQLExecutionError(RuntimeError):
    pass


def execute_immediate(sde, sql):
    try:
        sde_conn = arcpy.ArcSDESQLExecute(sde)
    except Exception as err:
        msg = arcpy.GetMessages() or str(err)
        raise SDEConnectionError(f"Failed to connect using SDE connection '{sde}': {msg}") from err

    try:
        result = sde_conn.execute(sql)
    except Exception as err:
        msg = arcpy.GetMessages() or str(err)
        raise SDESQLExecutionError(f"SQL execution failed for: {sql}\nArcPy message: {msg}") from err
    finally:
        del sde_conn

    return result


def execute_statements(sde
                      ,sqls):

    sde_conn = arcpy.ArcSDESQLExecute(sde)
    sde_conn.startTransaction()

    for sql in sqls:
        sde_conn.execute(sql)

    sde_conn.commitTransaction()


def selectavalue(sde,
                 sql):

    sdereturn = execute_immediate(sde,
                                  sql)

    if sdereturn is None:
        raise ValueError('Returned NULL from {0}'.format(sql))
    if isinstance(sdereturn, list):
        raise ValueError('Did not return single value on {0}'.format(sql))

    return sdereturn


def selectacolumn(sde,
                  sql):

    sdereturn = execute_immediate(sde,
                                  sql)

    if isinstance(sdereturn, bool) and sdereturn:
        return []
    if isinstance(sdereturn, (str, int, float, complex)):
        return [sdereturn]
    if isinstance(sdereturn, list):
        return [row[0] for row in sdereturn]
    if sdereturn is None:
        return [None]

    raise ValueError('Unknown return type from {0}'.format(sql))