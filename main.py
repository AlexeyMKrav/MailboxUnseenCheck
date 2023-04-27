import os
import imaplib
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

if __name__ == '__main__':
    IMAP_SERVER = os.environ.get('IMAP_SERVER')
    IMAP_USER = os.environ.get('IMAP_USER')
    IMAP_PASSWORD = os.environ.get('IMAP_PASSWORD')
    imap = imaplib.IMAP4_SSL(host=IMAP_SERVER)
    imap.login(IMAP_USER, IMAP_PASSWORD)
    imap.select(mailbox="INBOX", readonly=True)
    (status, ids) = imap.search(None, '(UNSEEN)')
    if status == 'OK':
        if ids[0]:
            last_id = ids[0].split()[-1]
            mail_date = bytes.decode(imap.fetch(last_id, '(BODY.PEEK[HEADER.FIELDS (Date)])')[1][0][1].strip())
            dt = datetime.strptime(mail_date, 'Date: %a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None)
            diff_dt = datetime.now() - dt

            print(diff_dt.seconds)
        else:
            print(0)
