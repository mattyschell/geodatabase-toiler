import sys
import smtplib
import datetime
import logging
import socket
from email.message import EmailMessage

import gdb

if __name__ == "__main__":

    if len(sys.argv) != 4:
        raise ValueError('Expected 3 inputs, notifyonsuccess flag, emailsto, emailfrom')

    notifyonsuccess = sys.argv[1]
    ptoemails       = sys.argv[2]
    pfromemail      = sys.argv[3]

    gdb2test = gdb.Gdb()
    msg = EmailMessage()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    success = False

    if not gdb2test.checkconnection(): 
        content =  'ESRI geodatabase on {0} is unreachable '.format(gdb2test.databasestring)
        msg['Subject'] = 'Unreachable ESRI Geodatabase'
    else:
        success = True
        content = 'ESRI geodatabase on {0} is reachable '.format(gdb2test.databasestring)    
        msg['Subject'] = 'Reachable ESRI Geodatabase'

    content += 'at {0} '.format(datetime.datetime.now())
    content += 'attempting to connect from {0} '.format(socket.gethostname())

    #always log
    logger.info(content)

    msg.set_content(content)
    msg['From'] = ptoemails
    msg['To'] = ptoemails

    if (not success or notifyonsuccess == 'Y'):
        s = smtplib.SMTP('doittsmtp.nycnet')
        s.send_message(msg)
        s.quit()



