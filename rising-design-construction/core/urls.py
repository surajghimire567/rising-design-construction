from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="services"),
    path("projects/", views.case_study_list, name="case_studies"),
    path("projects/<slug:slug>/", views.case_study_detail, name="case_study_detail"),
    path("about/", views.about, name="about"),
]
