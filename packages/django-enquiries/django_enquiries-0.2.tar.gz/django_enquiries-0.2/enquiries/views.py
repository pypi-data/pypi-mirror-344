from .forms import ContactUsForm
from django.contrib import messages
from django.views.generic import FormView
    
class BaseContactUsView(FormView):
    form_class = ContactUsForm
    template_name = 'enquiries/form.html'

    def form_valid(self, form):
        form.save()
        form.instance.send_email()
        messages.success(self.request, f'Your form has been successfully submitted. We will be in contact with you as soon as we can.')
        return super().form_valid(form)