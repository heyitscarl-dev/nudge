from fastapi import FastAPI
from nudge.controllers import incoming

app = FastAPI()
app.include_router(incoming.router)
