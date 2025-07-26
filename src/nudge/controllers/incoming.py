"""
the `mailin` controller is responsible for receiving
incoming mail from mailgun. this is done through
a webhook at `/webhook/mailin`. the actual processing
of these mails is defered to a later stage in the 
program.
"""

from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Form, HTTPException

from nudge.model.email import IncomingEmail
from nudge.utils import env


router = APIRouter()

@router.post("/webhook/incoming", status_code=202)
async def incoming(email: Annotated[IncomingEmail, Form()], background_tasks: BackgroundTasks):
    if not email.verify(env.MAILGUN_WEBHOOK_SIGNING_KEY):
        raise HTTPException(403, detail = "invalid signature")

    background_tasks.add_task(lambda: print("ignoring queued email."))
    return { "detail": "queued" }
