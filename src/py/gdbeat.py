import sys
import smtplib
import datetime
import logging
import socket
import os
from email.message import EmailMessage


if __name__ == "__main__":

    
    notifyonsuccess = sys.argv[1]
    ptoemails       = sys.argv[2]
    try:
        platform = sys.argv[3].lower()
    except:
        platform = 'oracle'
    try:
        dbname = sys.argv[4] 
    except:
        # C:\xxx\yyyy.sde 
        dbname = os.environ['SDEFILE']
    try:
        maintaineremails = sys.argv[5] 
    except:
        maintaineremails = ptoemails

    if platform.lower().startswith('oracle'):
        platform = 'oracle'

    emailfrom       = os.environ['NOTIFYFROM']
    smtpfrom        = os.environ['SMTPFROM']

    sdeconn = os.environ['SDEFILE']
    msg = EmailMessage()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # importing the (licensed) ESRI client side code is part of the round trip test
    importsuccess = True
    try:
        import gdb
    except ImportError:
        importsuccess = False
        content = 'Unknown if ESRI geodatabase on {0} is reachable. Module import failure. '.format(dbname)
        msg['Subject'] = 'Unknown ESRI Geodatabase'
    except Exception as e:
        importsuccess = False
        content =  'Unknown if ESRI geodatabase on {0} is reachable. '.format(dbname)
        content += 'Module import failure on {0}. '.format(socket.gethostname())
        content += 'Check the host and ESRI licensing '
        msg['Subject'] = 'Unknown ESRI Geodatabase'

    success = False

    if importsuccess:

        try:

            # failures will be in initialization 
            # do not use gdb2test outside of this block, it may be undefined

            gdb2test = gdb.Gdb(None
                              ,platform)
    
            if not gdb2test.checkconnection(): 
                success = False
            else:
                success = True    
        except:
            success = False

        if success:
            content = 'ESRI geodatabase on {0} is reachable '.format(dbname)    
            msg['Subject'] = 'Reachable ESRI Geodatabase'
        else:
            content =  'ESRI geodatabase on {0} is unreachable '.format(dbname)
            msg['Subject'] = 'Unreachable ESRI Geodatabase'

    content += 'at {0} '.format(datetime.datetime.now().strftime("%H:%M:%S"))
    content += 'attempting to connect from {0} '.format(socket.gethostname())

    # always log
    logger.info(content)

    msg.set_content(content)
    msg['From'] = emailfrom
    
    # this is headers only 
    # if a string is passed to sendmail it is treated as a list with one element!
    if importsuccess:
        msg['To'] = ptoemails
    else:
        # https://github.com/mattyschell/geodatabase-toiler/issues/20
        msg['To'] = maintaineremails

    if (not success or notifyonsuccess == 'Y'):
        smtp = smtplib.SMTP(smtpfrom)
        smtp.sendmail(msg['From'], msg['To'].split(","), msg.as_string())
        smtp.quit()

