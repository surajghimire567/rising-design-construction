from django import forms
from content.models import Service
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    # A low-friction honeypot. Real users never see or fill this field.
    website = forms.CharField(required=False, widget=forms.HiddenInput, label="")

    class Meta:
        model = Inquiry
        fields = ("name", "email", "phone", "project_type", "message", "attachment", "website")
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com"}),
            "phone": forms.TelInput(attrs={"autocomplete": "tel", "placeholder": "+977 ..."}),
            "project_type": forms.Select(),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Tell us about your project, location, timeline, and what you need."}),
            "attachment": forms.ClearableFileInput(attrs={"accept": ".pdf,.jpg,.jpeg,.png,.webp"}),
        }
        labels = {"project_type": "Project type", "attachment": "Drawing or specification (optional)"}
        help_texts = {"attachment": "PDF, JPG, PNG, or WebP; maximum 10 MiB. Uploaded files are private."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project_type"].queryset = Service.objects.filter(is_active=True).order_by("display_order", "title")
        self.fields["project_type"].empty_label = "Select a service"

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Unable to process this request.")
        return value
