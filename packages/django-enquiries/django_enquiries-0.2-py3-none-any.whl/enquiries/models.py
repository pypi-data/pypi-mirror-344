from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string

class BaseEnquiry(models.Model):
    TICKET_NUM_LEN = 4
    TEXT_FILE = "enquiries/email.txt"
    HMTL_FILE = "enquiries/email.html"
    BUSINESS_NAME = "Company"

    ticket_number = models.CharField(max_length=TICKET_NUM_LEN)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    message=models.TextField()
    date_created = models.DateField(default=timezone.now)
    is_closed = models.BooleanField(default=False)
    date_closed = models.DateField(blank=True, null=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    
    def mark_closed(self, closed_by):
        """Close the enquiry."""
        self.is_closed = True
        self.date_closed = timezone.now()
        self.closed_by = closed_by
    
    def reopen(self):
        """Reopen the enquiry."""
        self.is_closed = False
        self.date_closed = None
        self.closed_by = None

    def get_default_ticket_num(self):
        """(str) Return the default ticket number."""
        return "".zfill(self.TICKET_NUM_LEN)

    def set_ticket_number(self):
        """Set the enquiry's ticket number."""
        if self.ticket_number == self.get_default_ticket_num():
                self.ticket_number = str(self.pk).zfill(self.TICKET_NUM_LEN)
                self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.ticket_number = self.get_default_ticket_num()
        return super().save(*args, **kwargs)

    def send_email(self, text_file=TEXT_FILE, html_file=HMTL_FILE, from_email=None):
        """
        Send an automatic email to the user notifying them that their enquiry has been received.
        
        If from_email is None, try using the EMAIL_HOST_USER setting.
        """
        if not from_email:
            try:
                from_email = settings.EMAIL_HOST_USER
            except:
                raise ValueError("Set the EMAIL_HOST_USER setting or input a value for from_email.")
            
        context = {
            'ticket_number': self.ticket_number,
            'name': self.name,
            'message': self.message,
            'date_created': self.date_created,
            'from_email': from_email,
            'business_name': self.BUSINESS_NAME,
        }

        text_content = render_to_string(text_file, context)
        html_content = render_to_string(html_file, context)
        
        msg = mail.EmailMultiAlternatives(
            subject=f"Enquiry #{self.ticket_number}",
            body=text_content,
            from_email=from_email,
            to=[self.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
    class Meta:
        verbose_name_plural = "Enquiries"