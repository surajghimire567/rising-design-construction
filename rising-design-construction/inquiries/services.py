import json
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger("inquiries")


def send_inquiry_notification(inquiry):
    """Send via HTTPS API when configured; otherwise use Django's selected email backend."""
    body = (
        f"New consultation request #{inquiry.pk}\n\n"
        f"Name: {inquiry.name}\nEmail: {inquiry.email}\nPhone: {inquiry.phone}\n"
        f"Project type: {inquiry.project_type}\nSubmitted: {inquiry.created_at:%Y-%m-%d %H:%M %Z}\n\n"
        f"Message:\n{inquiry.message}\n\n"
        "The optional attachment is stored privately in the admin-managed media bucket."
    )
    try:
        if settings.RESEND_API_KEY:
            payload = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [settings.INQUIRY_NOTIFY_EMAIL],
                "subject": f"New consultation request #{inquiry.pk}",
                "reply_to": inquiry.email,
                "text": body,
            }
            request = Request(
                "https://api.resend.com/emails",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}", "Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=10) as response:
                if response.status >= 300:
                    raise RuntimeError(f"Email API returned HTTP {response.status}")
        else:
            send_mail(
                subject=f"New consultation request #{inquiry.pk}",
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.INQUIRY_NOTIFY_EMAIL],
                fail_silently=False,
                reply_to=[inquiry.email],
            )
    except (HTTPError, URLError, TimeoutError, OSError, RuntimeError, ValueError):
        # The database save is the source of truth; a mail outage must not discard a lead.
        logger.exception("Notification email failed for inquiry id=%s", inquiry.pk)
