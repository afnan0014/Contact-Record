from django import forms
from .models import Contact, PhoneNumber
from django.forms.models import inlineformset_factory

from django import forms
from .models import Contact, PhoneNumber
from django.forms.models import inlineformset_factory

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'address', 'image'] 

class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['number']
        widgets = {
            'number': forms.TextInput(attrs={'type': 'number', 'pattern': '[0-9]+', 'title': 'Enter numbers only'})
        }
        

    def clean_number(self):
        number = self.cleaned_data.get('number')

        if not number:
            raise forms.ValidationError("Phone number is required.")

        if not number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")

        if len(number) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")

        return number

# Formset for managing multiple phone numbers
PhoneNumberFormSet = inlineformset_factory(
    Contact,
    PhoneNumber,
    form=PhoneNumberForm,
    extra=1,
    can_delete=True
)
