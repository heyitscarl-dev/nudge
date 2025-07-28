from datetime import UTC, datetime
from jinja2 import Environment, FileSystemLoader
from nudge.model.email import IncomingEmail, OutgoingEmail

jenv = Environment(
    loader=FileSystemLoader("res/templates")
)

def render_reply(email: IncomingEmail) -> str:
    dt = datetime.fromtimestamp(email.timestamp, UTC)
    return jenv.get_template("reply.html").render(
        content=email.body_html,
        from_ = email.from_,
        date =  dt.strftime("%d.%m.%Y"),
        time = dt.strftime("%H:%M:%S")
    )

def render_email(content: str, reply: IncomingEmail | None) -> str:
    return jenv.get_template("email.html").render(
        content=content,
        reply = render_reply(reply) if reply else ""
    )
