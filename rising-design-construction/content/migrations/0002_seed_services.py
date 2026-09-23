from django.db import migrations

SERVICES = [
    ("Municipal drawings", "municipal-drawings", "Preparation of clear, coordinated municipal drawing packages to support planning and approval workflows.", "DRAW", True, 1),
    ("Construction", "construction", "Client-focused construction delivery with careful attention to quality, coordination, and project requirements.", "BUILD", True, 2),
    ("3D visualization", "3d-visualization", "Three-dimensional visualizations that help clients understand design intent before work begins.", "3D", True, 3),
    ("Interior design", "interior-design", "Thoughtful interior concepts that balance function, comfort, materials, and the character of each space.", "SPACE", True, 4),
    ("Construction supervision", "construction-supervision", "On-site supervision and progress coordination to help work follow the agreed drawings and specifications.", "SITE", True, 5),
    ("Structural analysis", "structural-analysis", "Structural assessment and engineering analysis to inform safe, practical building decisions.", "STRUCT", True, 6),
    ("Building documentation", "building-documentation", "Organized building documentation and drawing sets that make project information easier to review and use.", "DOCS", False, 7),
    ("Road and bridge construction", "road-bridge-construction", "Road and bridge construction services focused on sound coordination, quality, and long-term performance.", "CIVIL", False, 8),
]

def seed(apps, schema_editor):
    Service = apps.get_model("content", "Service")
    for title, slug, description, label, featured, order in SERVICES:
        Service.objects.update_or_create(slug=slug, defaults={
            "title": title, "description": description, "short_label": label,
            "is_active": True, "is_featured": featured, "display_order": order,
        })

class Migration(migrations.Migration):
    dependencies = [("content", "0001_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
