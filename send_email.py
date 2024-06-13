import smtplib
import os
from email.message import EmailMessage

email_id = 'asmaa.a.hakami@gmail.com' #os.environ.get('EMAIL_ADDR') # # 
email_pass = 'ADT12345' #os.environ.get('EMAIL_PASS') #  #

def send(file, new_email):
    msg = EmailMessage()
    msg['Subject'] = "Evaluation Result"
    msg['From'] = email_id
    msg['To'] = new_email # as.soma45@gmail.com
    msg.set_content("")

    files = [file]
    for file in files:
        with open(file,'rb') as m:
            file_data = m.read()
            file_name = m.name
        msg.add_attachment(file_data, maintype = 'image', subtype = 'octet-stream', filename = file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id , email_pass)
        smtp.send_message(msg)
