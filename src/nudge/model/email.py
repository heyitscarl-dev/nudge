from pydantic import BaseModel, Field
import hmac, hashlib

class IncomingEmail(BaseModel):
    """
    All data sent by mailgun regarding incoming emails.
    """

    recipient: str
    sender: str 
    from_: str                  = Field(alias="from")
    subject: str 
    body_plain: str             = Field(alias="body-plain")
    stripped_text: str          = Field(alias="stripped-text")
    body_html: str              = Field(alias="body-html")
    stripped_html: str          = Field(alias="stripped-html")
    timestamp: int
    token: str 
    signature: str
    message_headers: str        = Field(alias="message-headers")

    # todo: add attachment-N fields where N <= attachment_count
    #       potentially dynamic list added after initial parsing

    def verify(self, signing_key: str) -> bool:
        """
        Verify that the `IncomingEmail` is authentic and sent by Mailgun.

        mailgun signs requests with an HMAC SHA-256 hash of the
        concatenated timestamp and token, using a private "signing 
        key" as the secret. this function recreates this signature
        and matches it with the one provided in the request.

        Args:
            signing_key (str): the "HTTP webhook signing key" from your mailgun account
        
        Returns:
            bool: True if the signature is valid, False otherwise.
        """

        msg = f"{self.timestamp}{self.token}".encode()
        expected = hmac.new(key=signing_key.encode(), msg=msg, digestmod=hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, self.signature)

class OutgoingEmail(BaseModel):
    """
    All data that mailgun accepts for sending an email.
    """

    from_: str                      = Field(serialization_alias="from")
    to: str
    cc: list[str] | None            = Field(default=None)
    bcc: list[str] | None           = Field(default=None)
    subject: str 
    text: str | None                = Field(default=None)
    html: str | None                = Field(default=None)
    attachment: list[str] | None    = Field(default=None)
    inline: list[str] | None        = Field(default=None)
