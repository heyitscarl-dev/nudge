from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Form, HTTPException

from nudge.model.email import IncomingEmail
from nudge.model.message import Message
from nudge.services.message import process
from nudge.utils import environment

router = APIRouter()

@environment.with_get_environment("MAILGUN_HTTP_WEBHOOK_SIGNING_KEY")
@router.post("/webhook/incoming", status_code=202)
async def incoming(
        email: Annotated[IncomingEmail, Form()],
        tasks: BackgroundTasks,
        *,
        MAILGUN_HTTP_WEBHOOK_SIGNING_KEY: str
):
    """
    Receive incoming email addresses via a webhook, called by Mailgun.

    Args:
        email: The parsed email
        tasks: BackgroundTasks, provided by FastAPI
        MAILGUN_HTTP_WEBHOOK_SIGNING_KEY: The webhook signing key, needed to verify incoming calls.

    Returns:
        HTTP 202 if processing task queues successfully
        HTTP 403 if authorization fails
    """

    # verify that the incoming webhook call was 
    # actually dispatched by Mailgun
    if not email.verify(MAILGUN_HTTP_WEBHOOK_SIGNING_KEY):
        raise HTTPException(403, detail = "invalid signature")

    # now that we can be sure that Mailgun has sent 
    # a new email, we can queue a processing task 
    # to be asynchronously handled
    tasks.add_task(lambda: process(Message.from_incoming(email)))
    return { "detail": "queued" }
