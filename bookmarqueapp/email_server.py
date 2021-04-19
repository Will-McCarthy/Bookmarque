import smtplib, ssl, email
from email import encoders  # email import for sending emails
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import config as cfg # for loading in custom configuration information

# Email Initialization
try:
    gmail_server_user = cfg.email['user']
    gmail_server_password = cfg.email['password']
    #SMTP initialization and setups
    port = 465
    # Create a secure SSL context
    context = ssl.create_default_context()
    #Server connection
    server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
    server.login(gmail_server_user, gmail_server_password)
except Exception as ex:
    print("Email couldn't start: " + str(ex))

# send out param message with subject to either recipient or a dummy email if test_mode is True
def send_email(html_message, subject, recipient, test_mode=False):
    try:
        # Email Generation
        message = MIMEMultipart()
        message["From"] = gmail_server_user

        # if testing than send email to itself
        if test_mode:
            recipient = cfg.email['user']

        message["To"] = recipient
        message["Subject"] = subject
        msgAlternative = MIMEMultipart('alternative')
        msgText = MIMEText(html_message, 'html', 'utf-8') # inline html, which could be replaced with larger template files if needed
        msgAlternative.attach(msgText)
        message.attach(msgAlternative)

        # Print email to console and Send email
        print("Send out an email here")
        text = message.as_string()
        print(text)

        server.sendmail(gmail_server_user, recipient, text)
    except Exception as ex:
        print("Email could not be sent: " + str(ex))
