from nudge.model.message import Message, MessageBody
from nudge.utils import environment

from mailgun.client import Client

auth = ("api", environment.get_environment("MAILGUN_API_KEY"))
client = Client(auth=auth, api_url="https://api.eu.mailgun.net/")

@environment.with_get_environment("MAILGUN_DOMAIN")
def send(message: Message, *, MAILGUN_DOMAIN: str):
    data = message.to_outgoing().model_dump(by_alias=True)
    res = client.messages.create(data=data, domain=MAILGUN_DOMAIN)
    return res

def reply_with(message: Message, body: MessageBody, sender: str | None = None):
    reply = message.reply_with(body, sender=sender)
    send(reply)
