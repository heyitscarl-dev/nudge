from nudge.model.message import Message, MessageBody
from nudge.utils import env

from mailgun.client import Client

auth = ("api", env.MAILGUN_API_KEY)
client = Client(auth=auth, api_url="https://api.eu.mailgun.net/")

def send(message: Message):
    data = message.to_outgoing().model_dump(by_alias=True)
    res = client.messages.create(data=data, domain=env.MAILGUN_DOMAIN)
    return res

def reply_with(message: Message, body: MessageBody):
    reply = message.reply_with(body)
    send(reply)
