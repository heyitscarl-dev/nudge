from pydantic import BaseModel, Field
import hmac, hashlib

class IncomingEmail(BaseModel):
    """
    The data model for an incoming email webhook via Mailgun.
    """

    sender: str     = Field(alias="From")
    recipient: str  = Field(alias="To")
    
    subject: str 
    stripped: str   = Field(alias="stripped-text")

    # verification
    token: str
    timestamp: str 
    signature: str

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
