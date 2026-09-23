from django.db import models
from django.core.validators import RegexValidator
from content.models import Service
from core.storage import StorageAlias
from .validators import validate_consultation_upload

private_storage = StorageAlias("private_uploads")


class Inquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        REVIEWING = "reviewing", "Reviewing"
        CONTACTED = "contacted", "Contacted"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    phone = models.CharField(
        max_length=32,
        validators=[RegexValidator(r"^[+0-9() .-]{7,32}$", "Enter a phone number using digits and common phone symbols.")],
    )
    project_type = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="inquiries")
    message = models.TextField(max_length=5000)
    attachment = models.FileField(upload_to="requests/", storage=private_storage, blank=True, validators=[validate_consultation_upload])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "inquiries"

    def __str__(self):
        return f"Inquiry #{self.pk} — {self.name} ({self.get_status_display()})"
