from django import forms
from .models import BaseEnquiry

class ContactUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs["placeholder"] = "enter your name"
        self.fields['email'].widget.attrs["placeholder"] = "enter your email address"
        self.fields['message'].widget.attrs["placeholder"] = "enter your message"

    class Meta:
        model = BaseEnquiry
        fields = ['name', 'email', 'message']