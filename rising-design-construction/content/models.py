from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from core.storage import StorageAlias
from core.validators import validate_image_size, validate_pdf_file

public_storage = StorageAlias("public_media")


class Service(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField()
    short_label = models.CharField(max_length=40, blank=True, help_text="Short label or simple icon text; do not enter HTML.")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class CaseStudy(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.CharField(max_length=320)
    body = models.TextField(help_text="Plain text. Use blank lines for paragraphs; HTML is escaped in templates.")
    cover_image = models.ImageField(upload_to="case-studies/covers/", storage=public_storage, validators=[validate_image_size])
    report_pdf = models.FileField(
        upload_to="case-studies/reports/", storage=public_storage, blank=True,
        validators=[FileExtensionValidator(["pdf"]), validate_pdf_file],
        help_text="Optional public PDF report/drawing. Do not upload confidential files.",
    )
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="case_studies")
    project_date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-project_date", "title"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    client_name = models.CharField(max_length=120)
    company = models.CharField(max_length=160, blank=True)
    quote = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", storage=public_storage, blank=True, validators=[validate_image_size])
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "client_name"]

    def __str__(self):
        return f"{self.client_name} — {self.company}" if self.company else self.client_name


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.TextField()
    photo = models.ImageField(upload_to="team/", storage=public_storage, blank=True, validators=[validate_image_size])
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} — {self.role}"
