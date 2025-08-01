from typing import Callable
from nudge.model.message import Message, MessageBody
from nudge.services import openai
from nudge.services.mailgun import reply_with
from nudge.utils import environment
from nudge.view.loader import render_email

SEND_AS: Callable[[str], str] = lambda domain: f"Nudge <nudge@{domain}>"

@environment.with_get_environment("MAILGUN_DOMAIN")
def process(incoming: Message, *, MAILGUN_DOMAIN: str):
    plain = openai.get_response(incoming).output_text
    html = render_email(plain, reply = None)
    body = MessageBody(plain = plain, html = html)
    
    reply_with(incoming, body, sender=SEND_AS(MAILGUN_DOMAIN))
