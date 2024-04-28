import smtplib
from email.mime.text import MIMEText

sender = 'admin@btspti.com'
receivers = ['magoreal4@gmail.com']
message = MIMEText('This is a test email message.')

message['Subject'] = 'Test SMTP Email'
message['From'] = sender
message['To'] = ", ".join(receivers)

try:
    # Usar SMTP_SSL para iniciar directamente con SSL/TLS
    smtpObj = smtplib.SMTP_SSL('mail.btspti.com', 465, timeout=5)
    smtpObj.login(sender, 'admin10203040!')
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()
    print("Successfully sent email")
except smtplib.SMTPException as e:
    print(f"Error: unable to send email. Error: {e}")
