from twilio.rest import Client
import os
# Your Account SID from twilio.com/console
account_sid = os.environ['twilioSid'] #"AC1c538b493478040737a7f021594f2112"
# Your Auth Token from twilio.com/console
auth_token  = os.environ['twilioAuth'] #"4ff3806a2afa4d496d8890b396a7ae60"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+14017495246", 
    from_=os.environ['twilioPhone'], #"+17743571474 ",
    body="Hello from Python!")

print(message.sid)
