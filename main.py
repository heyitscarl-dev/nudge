from typing import Annotated
from fastapi import FastAPI, Form

from nudge.model.email import IncomingEmail
from nudge.utils import env

import dotenv
dotenv.load_dotenv()

app = FastAPI()

MAILGUN_WEBHOOK_SIGNING_KEY = env.get_environment("MAILGUN_WEBHOOK_SIGNING_KEY", "mailgun HTTP webhook signing key")

@app.post("/webhook/mailin", status_code=202)
async def mailin(
    email: Annotated[IncomingEmail, Form()]
):
    print(email.verify(MAILGUN_WEBHOOK_SIGNING_KEY))

    return { "status": "accepted (ignored)" }
