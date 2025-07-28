"""
the `mailin` controller is responsible for receiving
incoming mail from mailgun. this is done through
a webhook at `/webhook/mailin`. the actual processing
of these mails is defered to a later stage in the 
program.
"""

import markdown

from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Form, HTTPException

from nudge.model.email import IncomingEmail
from nudge.view import loader
from nudge.services import openai as openai_service
from nudge.services import mailgun as mailgun_service
from nudge.utils import env


router = APIRouter()

def process(email: IncomingEmail):
    text = openai_service.get_response(email).output_text
    html = markdown.markdown(text)
    mailgun_service.reply(email, loader.render_email(html, email))

@router.post("/webhook/incoming", status_code=202)
async def incoming(email: Annotated[IncomingEmail, Form()], background_tasks: BackgroundTasks):
    if not email.verify(env.MAILGUN_WEBHOOK_SIGNING_KEY):
        raise HTTPException(403, detail = "invalid signature")

    background_tasks.add_task(lambda: process(email))
    return { "detail": "queued" }
