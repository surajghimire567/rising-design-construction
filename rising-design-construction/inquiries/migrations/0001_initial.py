import core.storage
import inquiries.validators
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):
    initial = True
    dependencies = [("content", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Inquiry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(r"^[+0-9() .-]{7,32}$", "Enter a phone number using digits and common phone symbols.")])),
                ("message", models.TextField(max_length=5000)),
                ("attachment", models.FileField(blank=True, storage=core.storage.StorageAlias("private_uploads"), upload_to="requests/", validators=[inquiries.validators.validate_consultation_upload])),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("status", models.CharField(choices=[("new", "New"), ("reviewing", "Reviewing"), ("contacted", "Contacted"), ("closed", "Closed")], db_index=True, default="new", max_length=12)),
                ("project_type", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="inquiries", to="content.service")),
            ],
            options={"ordering": ["-created_at"], "verbose_name_plural": "inquiries"},
        ),
    ]
