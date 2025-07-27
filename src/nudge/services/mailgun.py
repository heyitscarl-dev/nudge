from pydantic import BaseModel, Field
from nudge.utils import env
from nudge.model.email import IncomingEmail
from mailgun.client import Client

REPLY_AS = "Nudge <nudge@mg.heyitscarl.dev>"

auth = ("api", env.MAILGUN_API_KEY)
client = Client(auth=auth, api_url="https://api.eu.mailgun.net/")

class OutgoingEmail(BaseModel):
    sender: str     = Field(serialization_alias="from")
    recipient: str  = Field(serialization_alias="to")
    subject: str
    html: str

def send(email: OutgoingEmail):
    data = email.model_dump(by_alias=True)
    res = client.messages.create(data=data, domain=env.MAILGUN_DOMAIN)
    return res

def reply(incoming: IncomingEmail, html: str):
    outgoing = OutgoingEmail( 
        sender = REPLY_AS,
        recipient = incoming.sender,
        subject = f"Re: {incoming.subject}",
        html = f"<html><body>{html} <div> {incoming.body}</body></html>"
     )

    send(outgoing)
