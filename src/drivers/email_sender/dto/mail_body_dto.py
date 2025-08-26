from pydantic import BaseModel

class MailBody(BaseModel):
    to: str
    subject: str
    body: str