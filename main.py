from fastapi import FastAPI
from nudge.controllers import incoming
from nudge.model.email import IncomingEmail
from nudge.services import mailgun
from pprint import pprint

app = FastAPI()
app.include_router(incoming.router)
