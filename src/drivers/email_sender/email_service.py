from src.drivers.email_sender.config import HOST, USERNAME, PASSWORD, PORT
from src.drivers.email_sender.dto.mail_body_dto import MailBody
from ssl import create_default_context
from email.message import EmailMessage
from smtplib import SMTP

class EmailService:

    def send_email(self, data: dict | None = None):
        msg_data = MailBody(**data)

        # Cria o e-mail usando EmailMessage
        message = EmailMessage()
        message.set_content(msg_data.body, subtype="html")
        message["From"] = USERNAME
        message["To"] = msg_data.to
        message["Subject"] = msg_data.subject

        ctx = create_default_context()

        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()