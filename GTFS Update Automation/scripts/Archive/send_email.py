from __future__ import print_function
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
#needed for attachment
import smtplib
import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import base64



# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.send'

# Email variables. Modify this!
EMAIL_FROM = 'transitanalystisrael@gmail.com'
EMAIL_TO = 'transitanalystisrael@gmail.com'

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message.attach(MIMEText(message_text, 'plain'))
    # message.attach(MIMEText(text_file_attachment, 'plain'))
    return message
        # {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def create_msg_and_send_email(email_subject, email_content, attached_file):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    :rtype: object
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))


    message = create_message(EMAIL_FROM, EMAIL_TO, email_subject, email_content)

    # attachement
    # It tells gmail which application it should use to read the attachement (it acts like an extension for windows).
    # If you dont provide it, you just wont be able to read the attachement (eg. a text) within gmail. You'll have to
    # download it to read it (windows will know how to read it with it's extension).
    my_mimetype, encoding = mimetypes.guess_type(attached_file)
    main_type, sub_type = my_mimetype.split('/', 1)  # split only at the first '/'

    # this part is used to tell how the file should be read and stored (r, or rb, etc.)
    if main_type == 'text':
        temp = open(attached_file, 'r')  # 'rb' will send this error: 'bytes' object has no attribute 'encode'
        attachement = MIMEText(temp.read(), _subtype=sub_type)
        temp.close()

    # encode the attachment, add a header and attach it to the message
    encoders.encode_base64(attachement)  # https://docs.python.org/3/library/email-examples.html
    filename = os.path.basename(attached_file)
    attachement.add_header('Content-Disposition', 'attachment', filename=filename)  # name preview in email
    message.attach(attachement)

    message_as_bytes = message.as_bytes() # the message should converted from string to bytes.
    message_as_base64 = base64.urlsafe_b64encode(message_as_bytes) #encode in base64 (printable letters coding)
    raw = message_as_base64.decode()  # need to JSON serializable (no idea what does it means)
    return {'raw': raw}

    sent = send_message(service, 'me', message)
    return sent




