# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['AC415c880ffd675018e0224be6f2ef70cb']
auth_token = os.environ['b85addb1aa26654806a1f5b18b640ed6']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+19894478965',
                     to='+919174005734'
                 )

print(message.sid)