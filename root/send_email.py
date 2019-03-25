"""
Send an e-mail with attachment to transitanalystisrael@gmail.com from transitanalystisrael@gmail.com
There's also an option to send an e-mail without an attachment
"""
import httplib2
import os
from oauth2client import client, tools, file
import base64

# needed for attachment
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apiclient import errors, discovery  #needed for gmail service
import boto3
from pathlib import Path
import time

def get_credentials(local_credentials_json, local_token_json):
    # get credentials from S3 bucket - this would only work on Transit Analyst EC2 that has a proper IAM role
    s3 = boto3.resource('s3')
    keys_buckets = s3.Bucket('transit-analyst-key-bucket')
    credentials_json = 'credentials.json'
    keys_buckets.download_file(credentials_json, local_credentials_json.as_posix())
    token_json = 'token.json'
    keys_buckets.download_file(token_json, local_token_json.as_posix())
    store = file.Storage(local_token_json.as_posix())
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(local_credentials_json, 'https://www.googleapis.com/auth/gmail.send')
        creds = tools.run_flow(flow, store)

    return creds




## Get creds, prepare message and send it
def create_message_and_send(sender, to, subject,  message_text_plain, attached_file):
    local_credentials_json = Path.cwd() / "assets" / "keys" / "credentials.json"
    local_token_json = Path.cwd() / "assets" / "keys" / "token.json"
    credentials = get_credentials(local_credentials_json, local_token_json)

    # Create an httplib2.Http object to handle our HTTP requests, and authorize it using credentials.authorize()
    http = httplib2.Http()

    # http is the authorized httplib2.Http() 
    http = credentials.authorize(http)        #or: http = credentials.authorize(httplib2.Http())

    service = discovery.build('gmail', 'v1', http=http)

    ## create messeage with attachment with attachment
    message_with_attachment = create_Message_with_attachment(sender, to, subject, message_text_plain, attached_file)
    send_Message_with_attachement(service, "me", message_with_attachment, message_text_plain,attached_file)

    #Deleting key files
    os.remove(local_credentials_json.as_posix())
    os.remove(local_token_json.as_posix())
    
def create_message_without_attachment (sender, to, subject, message_text_html, message_text_plain):
    # Create message container
    message = MIMEMultipart('alternative') # needed for both plain & HTML (the MIME type is multipart/alternative)
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = to

    # Create the body of the message (a plain-text and an HTML version)
    message.attach(MIMEText(message_text_plain, 'plain'))
    message.attach(MIMEText(message_text_html, 'html'))

    raw_message_no_attachment = base64.urlsafe_b64encode(message.as_bytes())
    raw_message_no_attachment = raw_message_no_attachment.decode()
    body  = {'raw': raw_message_no_attachment}
    return body



def create_Message_with_attachment(sender, to, subject, message_text_plain, attached_file):
    """Create a message for an email.

    message_text: The text of the email message.
    attached_file: The path to the file to be attached.

    Returns:
    An object containing a base64url encoded email object.
    """

    ##An email is composed of 3 part :
        #part 1: create the message container using a dictionary { to, from, subject }
        #part 2: attach the message_text with .attach() (could be plain and/or html)
        #part 3(optional): an attachment added with .attach() 

    ## Part 1
    message = MIMEMultipart() #when alternative: no attach, but only plain_text
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    ## Part 2   (the message_text)
    # The order count: the first (html) will be use for email, the second will be attached (unless you comment it)
    message.attach(MIMEText(message_text_plain, 'plain'))

    ## Part 3 (attachement) 
    # 3.1 get MimeType of attachment

    my_mimetype, encoding = mimetypes.guess_type(attached_file)

    # If the extension is not recognized it will return: (None, None)
    # If it's an .mp3, it will return: (audio/mp3, None) (None is for the encoding)
    #for unrecognized extension it set my_mimetypes to  'application/octet-stream' (so it won't return None again). 
    if my_mimetype is None or encoding is not None:
        my_mimetype = 'application/octet-stream' 


    main_type, sub_type = my_mimetype.split('/', 1)# split only at the first '/'   #

    # creating the attachement
    # this part is used to tell how the file should be read and stored (r, or rb, etc.)
    if main_type == 'text':
        temp = open(attached_file, 'r')  # 'rb' will send this error: 'bytes' object has no attribute 'encode'
        attachement = MIMEText(temp.read(), _subtype=sub_type, _charset='utf-8')
        temp.close()

    # 3.3 encode the attachment, add a header and attach it to the message
    encoders.encode_base64(attachement)
    filename = os.path.basename(attached_file)
    attachement.add_header('Content-Disposition', 'attachment', filename=filename) # name preview in email
    message.attach(attachement) 

    ## Part 4 encode the message (the message should be in bytes)
    message_as_bytes = message.as_bytes() # the message should converted from string to bytes.
    message_as_base64 = base64.urlsafe_b64encode(message_as_bytes) #encode in base64 (printable letters coding)
    raw = message_as_base64.decode()  # need to JSON serializable (no idea what does it means)
    return {'raw': raw} 



# def send_Message_without_attachement(service, user_id, body, message_text_plain):
    # try:
        # message_sent = (service.users().messages().send(userId=user_id, body=body).execute())
        # message_id = message_sent['id']
        # # print(attached_file)
        # print (f'Message sent (without attachment) \n\n Message Id: {message_id}\n\n Message:\n\n {message_text_plain}')
        # # return body
    # except errors.HttpError as error:
        # print (f'An error occurred: {error}')




def send_Message_with_attachement(service, user_id, message_with_attachment, message_text_plain, attached_file):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message_sent = (service.users().messages().send(userId=user_id, body=message_with_attachment).execute())
        message_id = message_sent['id']
        print("Message was sent with log. Message ID: ", message_id)

        # return message_sent
    except errors.HttpError as error:

        print (f'An error occurred: {error}')

def create_msg_and_send_email(subject, message, attached_file):
    to = 'transitanalystisrael@gmail.com'
    sender = 'transitanalystisrael@gmail.com'
    create_message_and_send(sender, to, subject, message, attached_file)
