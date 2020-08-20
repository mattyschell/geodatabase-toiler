# helper for test_doitt_sde_term_session.py
# shell out to this guy to execut a hanging session to be sniped
# CALL C:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\py\test_doitt_sde_term_session_sleeper.py "T:\GIS\Internal\Connections\oracle19c\dev\CSCL-ditCSdv1\mschell_private\mschell.sde"

import sys
import os
import cx_sde

sleeptimer=100

def main(sdefile):
    
    sql = """begin """ \
          """   sys.DBMS_SESSION.sleep({0}); """ \
          """end; """.format(sleeptimer)

    sdereturn = cx_sde.execute_immediate(sdefile,
                                         sql)


if __name__ == "__main__":

    psdefile = os.path.normpath(sys.argv[1])

    main(psdefile)

