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

    if not isinstance(sdereturn, list) and sdereturn is None:
        raise ValueError('Returned NULL from {0}'.format(sql))
    if not isinstance(sdereturn, list):
        return sdereturn
    else:
        raise ValueError('Did not return single value on {0}'.format(sql))


def selectacolumn(sde,
                  sql):

    sdereturn = execute_immediate(sde,
                                  sql)

    output = []

    if isinstance(sdereturn, bool) and sdereturn:

        return output

    elif isinstance(sdereturn, str):

        # just one value
        # be consistent and return a
        output = [sdereturn]
        return output

    elif isinstance(sdereturn, (int, float, complex)):

        # just one value
        # be consistent and return a
        output = [sdereturn]
        return output

    elif isinstance(sdereturn, list):

        # list of lists, but we only have one column
        for val in sdereturn:
            output.append(val[0])

        return output

    elif sdereturn is None:

        # just returned null

        output = [None]

        return output

    else:

        raise ValueError('Unknown return type from {0}'.format(sql))