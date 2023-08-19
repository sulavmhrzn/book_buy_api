from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from config.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USERNAME,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM="bookbuy@admin.com",
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_FROM_NAME="BookBuy",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(subject: str, recipients: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[recipients],
        body=body,
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
