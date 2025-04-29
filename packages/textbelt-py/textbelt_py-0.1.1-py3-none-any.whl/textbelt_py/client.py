import datetime
import hashlib
import hmac
import json
import time

from requests import Session
from requests.adapters import HTTPAdapter, Retry

from .schema import SMSRequest, SMSResponse, SMSStatusResponse, WebhookPayload


class TextbeltClient:
    """
    Textbelt API client.

    Send, recevie, and interact with Textbelt API.
    Requires a Textbelt API key as well as a requests.Session
    object to make http requests. If session not provided,
    it defaults to a session confgiured to make 3 retries with a backoff-factor of 1.

    Attributes:
        api_key (str): required textbelt api key.
        session (Session): requests.Session object used to make api requests.
    """

    BASE_URL = "https://textbelt.com"

    def __init__(self, api_key: str, session: Session | None = None) -> None:
        """
        Initialize Textbelt client instance.

        Args:
            api_key (str): required textbelt api key.
            session (Session | None): optional Session object used to make api requests.
        """

        self.api_key = api_key
        self.session = session if session else self._create_session()

    def send_sms(self, sms_request: SMSRequest) -> SMSResponse:
        """
        Send an SMS to a phone number.

        Function reads the phone, message, and optionally, the sender,
        and makes a POST request to Textbelt API to send a message.

        Args:
            sms_request (SMSRequest): request parameters used to create
                payload for Textbelt API.

        Returns:
            An instance of SMSResponse that holds the response data
            returned from the API call made to Textbelt.

        Raises:
            HTTPError: error thrown from requests on http failures.
        """
        send_sms_url = f"{self.BASE_URL}/text"

        payload = {
            "phone": sms_request.phone,
            "message": sms_request.message,
            "key": self.api_key,
        }

        if sms_request.sender:
            payload["sender"] = sms_request.sender

        resp = self.session.post(send_sms_url, payload)

        resp.raise_for_status()

        json_resp = resp.json()

        return SMSResponse(
            success=json_resp.get("success"),
            quota_remaining=json_resp.get("quotaRemaining"),
            text_id=json_resp.get("textId"),
            error=json_resp.get("error"),
        )

    def send_sms_with_reply_webhook(self, sms_request: SMSRequest) -> SMSResponse:
        """
        Send an SMS with reply webhook for responses to a phone number.

        Function reads the phone, message, reply_webhook_url, and optionally,
        the sender and webhook_data, and makes a POST request to Textbelt API
        to send a message. The reply webhook url is called when the recipient
        responds to the SMS.

        Args:
            sms_request (SMSRequest): request parameters used to create
                payload for Textbelt API.

        Returns:
            An instance of SMSResponse that holds the response data
            returned from the API call made to Textbelt.

        Raises:
            HTTPError: error thrown from requests on http failures.
        """
        send_sms_url = f"{self.BASE_URL}/text"

        payload = {
            "phone": sms_request.phone,
            "message": sms_request.message,
            "replyWebhookUrl": sms_request.reply_webhook_url,
            "key": self.api_key,
        }

        if sms_request.webhook_data:
            payload["webhookData"] = sms_request.webhook_data

        if sms_request.sender:
            payload["sender"] = sms_request.sender

        resp = self.session.post(send_sms_url, payload)

        resp.raise_for_status()

        json_resp = resp.json()

        return SMSResponse(
            success=json_resp.get("success"),
            quota_remaining=json_resp.get("quotaRemaining"),
            text_id=json_resp.get("textId"),
            error=json_resp.get("error"),
        )

    def verify_webhook(
        self, request_timestamp: str, request_signature: str, request_payload: str
    ) -> tuple[bool, WebhookPayload | None]:
        """
        Verify incoming textbelt webhook.

        Function verfies that the reply webhook request made by Textbelt
        is not forged or expired and is a valid request. Verification is done by first,
        checking that the request timestamp is within the 15 minute time limit.
        Then compares the request signature with the calculated signature
        for a match.

        Args:
            request_timestamp (str): UNIX timestamp as string from webhook request headers (X-textbelt-timestamp).
            request_signature (str): hmac signature as string from webhook request headers (X-textbelt-signature)
            request_payload (str): raw json payload as string from webhook request body.

        Returns:
            A boolean and WebhookPayload object dentoing verification status.
            If webhook not valid, returns False, None.
            Otherwise returns True and a WebhookPayload containing the parsed json
            payload data.
        """
        timestamp = int(request_timestamp)
        current_time = int(time.time())

        # time limit for a valid webhook request is 15 minutes.
        if current_time - timestamp > datetime.timedelta(minutes=15).seconds:
            return False, None

        signature = hmac.new(
            self.api_key.encode("utf-8"),
            (request_timestamp + request_payload).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        signature_is_valid = hmac.compare_digest(request_signature, signature)
        if not signature_is_valid:
            return False, None

        payload_json = json.loads(request_payload)
        return True, WebhookPayload(
            text_id=payload_json.get("textId"),
            from_number=payload_json.get("fromNumber"),
            text=payload_json.get("text"),
            data=payload_json.get("data"),
        )

    def check_sms_delivery_status(self, text_id: str) -> SMSStatusResponse:
        """
        Check delivery status of an SMS.

        Function can be used to check the delvivery status of
        and SMS message that was sent. Uses the given
        text_id to find the status.

        Args:
            text_id (str): id of sms message to check status for.

        Returns:
            An SMSStatusResponse object denoting the text message's
            current delivery status.
        """
        sms_status_url = f"{self.BASE_URL}/status/{text_id}"

        resp = self.session.get(sms_status_url)

        resp.raise_for_status()

        json_resp = resp.json()

        return SMSStatusResponse(status=json_resp.get("status"))

    def _create_session(self) -> Session:
        retry = Retry(total=3, backoff_factor=1)
        retry_adapter = HTTPAdapter(max_retries=retry)
        session = Session()
        session.mount("http://", retry_adapter)
        session.mount("https://", retry_adapter)

        return session
