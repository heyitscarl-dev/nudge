from nudge.model.message import Message, MessageBody
from nudge.services import openai
from nudge.services.mailgun import reply_with
from nudge.utils import env
from nudge.view.loader import render_email

SEND_AS= f"Nudge <nudge@{env.MAILGUN_DOMAIN}>"

def process(incoming: Message):
    plain = openai.get_response(incoming).output_text
    html = render_email(plain, reply = None)
    body = MessageBody(plain = plain, html = html)
    
    reply_with(incoming, body, sender=SEND_AS)
