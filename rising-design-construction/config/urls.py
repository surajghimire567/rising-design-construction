from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

admin.site.site_header = "Rising Design and Construction administration"
admin.site.site_title = "Rising Design admin"
admin.site.index_title = "Website content and inquiries"


def health_check(request):
    return HttpResponse("ok", content_type="text/plain")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("", include("core.urls")),
    path("", include("inquiries.urls")),
]
