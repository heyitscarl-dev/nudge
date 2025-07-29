from openai import OpenAI
from nudge.model.message import Message
from nudge.utils import env

client = OpenAI(api_key=env.OPENAI_API_KEY)

def get_response(email: Message):
    response = client.responses.create(
        model="gpt-4o",
        instructions="You are a digital assistant called nudge. You are tasked with responding to incoming emails appropriately and in a useful manner. Note that these emails are sent to you specifically and not your client / superior. If you are not addressed directly in the mail, assume the mail is addressed to you. If the mail is addressed to someone else, assume it was forwarded to you. You may use markdown formatting.",
        input=f"{email.subject}\n\n{email.body.plain}"
    )

    return response
