from openai import OpenAI
from nudge.utils import env
from nudge.model.email import IncomingEmail

client = OpenAI(api_key=env.OPENAI_API_KEY)

def respond_to_email(email: IncomingEmail):
    response = client.responses.create(
        model="gpt-4o",
        instructions="You are a digital assistant called nudge. You are tasked with responding to incoming emails appropriately and in a useful manner. Note that these emails are sent to you specifically and not your client / superior. If you are not addressed directly in the mail, assume the mail is addressed to you. If the mail is addressed to someone else, assume it was forwarded to you.",
        input=f"{email.subject}\n\n{email.body}"
    )

    return response
