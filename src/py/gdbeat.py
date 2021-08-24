import sys
import smtplib
import datetime
import logging
import socket
import os
from email.message import EmailMessage

import gdb

if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise ValueError('Expected 2 inputs, notifyonsuccess flag, emailsto')

    notifyonsuccess = sys.argv[1]
    ptoemails       = sys.argv[2]
    emailfrom       = os.environ['NOTIFYFROM']
    smtpfrom        = os.environ['SMTPFROM']

    sdeconn = os.environ['SDEFILE']
    msg = EmailMessage()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    success = False

    try:

        # failures will be in initialization 
        # do not use gdb2test outside of this block, it may be undefined

        gdb2test = gdb.Gdb()
    
        if not gdb2test.checkconnection(): 
            success = False
        else:
            success = True    
    except:
        success = False

    if success:
        content = 'ESRI geodatabase on {0} is reachable '.format(sdeconn)    
        msg['Subject'] = 'Reachable ESRI Geodatabase'
    else:
        content =  'ESRI geodatabase on {0} is unreachable '.format(sdeconn)
        msg['Subject'] = 'Unreachable ESRI Geodatabase'

    content += 'at {0} '.format(datetime.datetime.now())
    content += 'attempting to connect from {0} '.format(socket.gethostname())

    # always log
    logger.info(content)

    msg.set_content(content)
    msg['From'] = emailfrom
    
    # this is headers only 
    # if a string is passed to sendmail it is treated as a list with one element!
    msg['To'] = ptoemails

    if (not success or notifyonsuccess == 'Y'):
        smtp = smtplib.SMTP(smtpfrom)
        smtp.sendmail(msg['From'], msg['To'].split(","), msg.as_string())
        smtp.quit()

