"""
The 'incoming' controller is responsible for 
receiving incoming emails from the a mailgun 
route, and queuing them to be processed.
"""

from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Form, HTTPException

from nudge.model.email import IncomingEmail
from nudge.model.message import Message
from nudge.services.message import process
from nudge.utils import env

router = APIRouter()

@router.post("/webhook/incoming", status_code=202)
async def incoming(email: Annotated[IncomingEmail, Form()], background_tasks: BackgroundTasks):
    if not email.verify(env.MAILGUN_WEBHOOK_SIGNING_KEY):
        raise HTTPException(403, detail = "invalid signature")

    background_tasks.add_task(lambda: process(Message.from_incoming(email)))
    return { "detail": "queued" }
