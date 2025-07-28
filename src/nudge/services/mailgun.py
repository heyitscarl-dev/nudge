from nudge.utils import env
from nudge.model.email import IncomingEmail, OutgoingEmail
from mailgun.client import Client

REPLY_AS = "Nudge <nudge@mg.heyitscarl.dev>"

auth = ("api", env.MAILGUN_API_KEY)
client = Client(auth=auth, api_url="https://api.eu.mailgun.net/")

def send(email: OutgoingEmail):
    data = email.model_dump(by_alias=True)
    res = client.messages.create(data=data, domain=env.MAILGUN_DOMAIN)
    return res

def reply(incoming: IncomingEmail, content: str):
    outgoing = OutgoingEmail(
        from_ = REPLY_AS,
        to=incoming.from_,
        subject=f"Re: {incoming.subject}",
        html=content
    )

    send(outgoing)
