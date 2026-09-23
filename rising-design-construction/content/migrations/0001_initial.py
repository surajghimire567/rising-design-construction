import django.core.validators
import django.utils.timezone
import core.storage
import core.validators
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("slug", models.SlugField(max_length=180, unique=True)),
                ("description", models.TextField()),
                ("short_label", models.CharField(blank=True, help_text="Short label or simple icon text; do not enter HTML.", max_length=40)),
                ("is_active", models.BooleanField(default=True)),
                ("is_featured", models.BooleanField(default=False)),
                ("display_order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["display_order", "title"]},
        ),
        migrations.CreateModel(
            name="CaseStudy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("summary", models.CharField(max_length=320)),
                ("body", models.TextField(help_text="Plain text. Use blank lines for paragraphs; HTML is escaped in templates.")),
                ("cover_image", models.ImageField(storage=core.storage.StorageAlias("public_media"), upload_to="case-studies/covers/", validators=[core.validators.validate_image_size])),
                ("report_pdf", models.FileField(blank=True, help_text="Optional public PDF report/drawing. Do not upload confidential files.", storage=core.storage.StorageAlias("public_media"), upload_to="case-studies/reports/", validators=[django.core.validators.FileExtensionValidator(["pdf"]), core.validators.validate_pdf_file])),
                ("project_date", models.DateField(default=django.utils.timezone.localdate)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("service", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="case_studies", to="content.service")),
            ],
            options={"ordering": ["-project_date", "title"]},
        ),
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("client_name", models.CharField(max_length=120)),
                ("company", models.CharField(blank=True, max_length=160)),
                ("quote", models.TextField()),
                ("photo", models.ImageField(blank=True, storage=core.storage.StorageAlias("public_media"), upload_to="testimonials/", validators=[core.validators.validate_image_size])),
                ("is_featured", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at", "client_name"]},
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("role", models.CharField(max_length=120)),
                ("bio", models.TextField()),
                ("photo", models.ImageField(blank=True, storage=core.storage.StorageAlias("public_media"), upload_to="team/", validators=[core.validators.validate_image_size])),
                ("display_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["display_order", "name"]},
        ),
    ]
