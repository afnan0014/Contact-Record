from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact  # use our Contact model
        fields = ['name', 'phone', 'email', 'address']  # these fields will be shown in the form
