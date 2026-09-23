from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .forms import InquiryForm
from .services import send_inquiry_notification


def _is_htmx(request):
    return request.headers.get("HX-Request", "").lower() == "true"


@require_http_methods(["GET", "POST"])
def consultation_request(request):
    is_htmx = _is_htmx(request)
    if request.method == "POST":
        form = InquiryForm(request.POST, request.FILES)
        if form.is_valid():
            inquiry = form.save()
            send_inquiry_notification(inquiry)
            if is_htmx:
                return render(request, "partials/inquiry_success.html", {"inquiry": inquiry})
            return redirect("inquiry_success")
        if is_htmx:
            # Keep status=200 so HTMX swaps the rendered field errors by default.
            return render(request, "partials/inquiry_form.html", {"form": form})
    else:
        form = InquiryForm()
    context = {
        "meta_title": "Request a consultation | Rising Design and Construction",
        "meta_description": "Tell us about your engineering, design, or construction project and request a consultation.",
        "form": form,
    }
    if is_htmx:
        return render(request, "partials/inquiry_form.html", context)
    return render(request, "pages/consultation.html", context)


@require_http_methods(["GET"])
def consultation_success(request):
    return render(request, "pages/inquiry_success_page.html", {
        "meta_title": "Request received | Rising Design and Construction",
        "meta_description": "Your consultation request has been received.",
    })
