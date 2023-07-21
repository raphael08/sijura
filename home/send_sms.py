import os
from twilio.rest import Client

from .sms import account_sids,auth_tokens
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def send_sms():
    account_sid = account_sids
    auth_token = auth_tokens
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Welcome.",
                        from_='+12175599495',
                        to='+255656569880'
                    )

    print("message sent")