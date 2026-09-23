from django.urls import path
from .views import consultation_request, consultation_success

urlpatterns = [
    path("consultation/", consultation_request, name="consultation"),
    path("consultation/received/", consultation_success, name="inquiry_success"),
]
