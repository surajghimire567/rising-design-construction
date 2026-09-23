from django.http import Http404
from django.shortcuts import get_object_or_404, render
from content.models import CaseStudy, Service, TeamMember, Testimonial


def home(request):
    context = {
        "meta_title": "Engineering, design and construction | Rising Design and Construction",
        "meta_description": "Municipal drawings, construction, visualization, interior design, supervision and structural services in Kathmandu, Nepal.",
        "services": Service.objects.filter(is_active=True, is_featured=True)[:6],
        "case_studies": CaseStudy.objects.select_related("service").order_by("-project_date")[:3],
        "testimonials": Testimonial.objects.filter(is_featured=True).order_by("-created_at")[:3],
    }
    return render(request, "pages/home.html", context)


def service_list(request):
    return render(request, "pages/services.html", {
        "meta_title": "Our services | Rising Design and Construction",
        "meta_description": "Explore engineering, design and construction services delivered by Rising Design and Construction.",
        "services": Service.objects.filter(is_active=True),
    })


def case_study_list(request):
    return render(request, "pages/case_studies.html", {
        "meta_title": "Selected projects | Rising Design and Construction",
        "meta_description": "Selected engineering, design and construction projects by Rising Design and Construction.",
        "case_studies": CaseStudy.objects.select_related("service").order_by("-project_date"),
    })


def case_study_detail(request, slug):
    study = get_object_or_404(CaseStudy.objects.select_related("service"), slug=slug)
    return render(request, "pages/case_study_detail.html", {
        "meta_title": f"{study.title} | Rising Design and Construction",
        "meta_description": study.summary,
        "study": study,
    })


def about(request):
    return render(request, "pages/about.html", {
        "meta_title": "About our team | Rising Design and Construction",
        "meta_description": "Meet the people behind Rising Design and Construction and learn how we work.",
        "team_members": TeamMember.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_featured=True).order_by("-created_at")[:3],
    })
