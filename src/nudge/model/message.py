from typing import Self
from nudge.model.email import IncomingEmail, OutgoingEmail

from pydantic import BaseModel

class MessageBody(BaseModel):
    """
    Represents the body or content of a 
    message. 

    Attributes:
        plain(str): The plain-text version of the message body. 
        html(str | None): The HTML, display-only version of the message body, if available.
    """

    plain: str
    html: str | None    = None

    @classmethod
    def from_incoming(cls, email: IncomingEmail) -> Self:
        return cls(plain = email.body_plain, html = email.body_html)

class Message(BaseModel):
    """
    Represents a single unit of communication
    between nudge and a user.

    Attributes:
        sender(str): Where the message originated from (usually the "from" field of an email)
        recipient(str): Who the message was addressed to
        subject(str): The subject line of the email.
        body(MessageBody): The message content, including plain-text and html variants.
    """

    sender: str
    recipient: str

    subject: str
    body: MessageBody

    @classmethod
    def from_incoming(cls, email: IncomingEmail) -> Self:
        return cls(
            sender=email.from_, 
            recipient=email.recipient, 
            subject=email.subject, 
            body=MessageBody.from_incoming(email)
        )

    def to_outgoing(self) -> OutgoingEmail:
        return OutgoingEmail(
            from_ = self.sender,
            to = self.recipient,
            subject = self.subject,
            text=self.body.plain,
            html=self.body.html
        )

    def reply_with(self, body: MessageBody, sender: str | None = None):
        return Message(
            sender=sender or self.recipient,
            recipient=self.sender,
            subject=f"Re: {self.subject}",
            body=body
        )
