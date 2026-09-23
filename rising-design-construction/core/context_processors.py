from django.conf import settings


def brand_context(request):
    return {
        "debug": settings.DEBUG,
        "business_name": "Rising Design and Construction",
        "business_tagline": "We design. We plan. We build. We deliver.",
        "business_phone": "+977 9843069355",
        "business_email": "risingdesignandconstruction@gmail.com",
        "business_address": "Tiniple, Tarakeshwor, Kathmandu, Nepal",
    }
