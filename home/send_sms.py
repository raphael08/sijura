# import os
# from twilio.rest import Client


# from decouple import config


# account_sids = config("account_sids")
# auth_tokens = config("auth_tokens")
# # from .sms import account_sids,auth_tokens
# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure

# def send_sms(number,code,room):
#     account_sid = account_sids
#     auth_token = auth_tokens
#     client = Client(account_sid, auth_token)

#     message = client.messages \
#                     .create(
#                         body=f"WELCOME TO SIJURA LODGE THANKS FOR BOOKING ROOM NO.{room} .. YOUR CONFIRMATION CODE IS {code}",
#                         from_= '+12175599495',
#                         to=number
#                     )

#     print("message sent")
    
    
    
