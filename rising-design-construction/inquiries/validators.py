from pathlib import Path
from PIL import Image, UnidentifiedImageError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_FORMATS = {
    ".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP",
}


def validate_consultation_upload(upload):
    if upload.size > MAX_UPLOAD_BYTES:
        raise ValidationError(_("Please keep the attachment at or below 10 MiB."))
    suffix = Path(upload.name).suffix.lower()
    if suffix == ".pdf":
        header = upload.read(5)
        upload.seek(0)
        if header != b"%PDF-":
            raise ValidationError(_("The file is not a valid PDF."))
        return
    expected = ALLOWED_IMAGE_FORMATS.get(suffix)
    if expected is None:
        raise ValidationError(_("Allowed files: PDF, JPG/JPEG, PNG, and WebP."))
    try:
        image = Image.open(upload)
        actual = image.format
        image.verify()
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        raise ValidationError(_("The uploaded image is invalid or could not be read."))
    finally:
        upload.seek(0)
    if actual != expected:
        raise ValidationError(_("The image content does not match its file extension."))
