from enum import Enum
from typing import Annotated

from pydantic import BaseModel, StringConstraints


class SMSRequest(BaseModel):
    """
    SMS request data used to send a text message.

    Pydanic model to represent the request
    parameters required to send an SMS
    via Textbelt API.

    Attributes:
        phone (str): the recipient phone number in E.164 format.
        message (str): test message content to send.
        sender (str | None): optional name of the entity sending SMS.
        reply_webhook_url (str | None): optional callback url to request if/when
            recipient responds to SMS.
        webhook_data (str | None): reply webhook data to send on reply webhook callback.
            Max length of 100 characters.
    """

    phone: str
    message: str
    sender: str | None = None
    reply_webhook_url: str | None = None
    webhook_data: Annotated[
        str | None,
        StringConstraints(max_length=100),
    ] = None


class SMSResponse(BaseModel):
    """
    SMS response data returned when text message is sent.

    Pydantic model to represent the response
    received from Textbelt API after sending
    an SMS message.

    Attributes:
        success (bool): true when message sent successfully,
            false otherwise.
        quota_remaining (int): number of messages remaining on account.
        text_id (str | None): optional id of the text sent to recipient when
            success is true.
        error (str | None): optional error message when success is false.
    """

    success: bool
    quota_remaining: int
    text_id: str | None = None
    error: str | None = None


class WebhookPayload(BaseModel):
    """
    Reply webhook payload.

    Pydantic model to represent the payload
    json request body sent to the webhook url
    when handling recipient response to
    an SMS message.

    Attributes:
        text_id (str): the id of the original text that began the conversation.
        from_number (str): the phone number of the user that sent the reply.
        text (str): the message content of the responder's reply.
        data (str): the custom webhook data set when orginal SMS sent to recipient.
    """

    text_id: str
    from_number: str
    text: str
    data: str


class Status(str, Enum):
    DELIVERED = "DELIVERED"
    SENT = "SENT"
    SENDING = "SENDING"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class SMSStatusResponse(BaseModel):
    status: Status
