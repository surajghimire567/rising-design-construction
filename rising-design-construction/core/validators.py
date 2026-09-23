from pathlib import Path
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_PUBLIC_PDF_BYTES = 20 * 1024 * 1024


def validate_image_size(upload):
    if upload.size > MAX_IMAGE_BYTES:
        raise ValidationError(_("Image must be no larger than 8 MiB."))


def validate_pdf_file(upload):
    if upload.size > MAX_PUBLIC_PDF_BYTES:
        raise ValidationError(_("PDF must be no larger than 20 MiB."))
    if Path(upload.name).suffix.lower() != ".pdf":
        raise ValidationError(_("Only PDF files are accepted."))
    head = upload.read(5)
    upload.seek(0)
    if head != b"%PDF-":
        raise ValidationError(_("The uploaded file does not have a valid PDF signature."))
