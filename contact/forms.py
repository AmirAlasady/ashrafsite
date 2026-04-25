from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot — must remain empty. Real users never see it (CSS-hidden in
    # the template); naive bots fill every field and get rejected.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
            }
        ),
        label="",
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Spam detected.")
        return cleaned
