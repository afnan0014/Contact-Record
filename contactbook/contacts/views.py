from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contact
from .forms import ContactForm
from django.db.models import Q
from django.db.models import Count

# SIGNUP VIEW
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()         # Create new user
            login(request, user)       # Log in the user
            return redirect('list_contacts')
    else:
        form = UserCreationForm()
    return render(request, 'contacts/signup.html', {'form': form})


# LOGIN VIEW
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_contacts')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'contacts/login.html', {'form': form})



# LOGOUT VIEW
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Contact, PhoneNumber  # Import your models

from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Contact, PhoneNumber

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Contact

@login_required
def list_contacts(request):
    search_query = request.GET.get('search', '')

    # Base queryset: all contacts of the user, ordered by name
    contacts = Contact.objects.filter(user=request.user).order_by('name')

    # Apply search if present
    if search_query:
        contacts = contacts.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(phone_numbers__number__icontains=search_query)
        ).distinct()

    # Pagination: 9 contacts per page
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contacts/contact_list.html', {
        'contacts': page_obj,  # Paginated contacts
        'search_query': search_query,
        'total_contacts': paginator.count,
        'page_obj': page_obj,  # Needed for page navigation in template
    })




from django.contrib import messages
from django.db.models import Q
from .models import Contact, PhoneNumber
from .forms import ContactForm, PhoneNumberFormSet
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        formset = PhoneNumberFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            contact_name = form.cleaned_data['name']
            phone_numbers = [
                f.cleaned_data.get('number')
                for f in formset
                if f.cleaned_data and not f.cleaned_data.get('DELETE', False)
            ]
            if request.POST.get('delete_image') and contact.image:
                contact.image.delete()
                contact.image = None

            if Contact.objects.filter(user=request.user, name__iexact=contact_name).exists():
                messages.error(request, f"⚠️ A contact named '{contact_name}' already exists.")
            elif PhoneNumber.objects.filter(contact__user=request.user, number__in=phone_numbers).exists():
                messages.error(request, "⚠️ One or more of these phone numbers already exist in your contacts.")
            else:
                contact = form.save(commit=False)
                contact.user = request.user
                contact.save()
                formset.instance = contact
                formset.save()
                messages.success(request, "✅ Contact added successfully!")
                return redirect('list_contacts')
    else:
        form = ContactForm()
        formset = PhoneNumberFormSet(queryset=PhoneNumber.objects.none())

    return render(request, 'contacts/contact_form.html', {
        'form': form,
        'formset': formset,
        'empty_form': formset.empty_form,
        'home_button': True
    })









# EDIT CONTACT VIEW (Protected)
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .models import Contact, PhoneNumber
from .forms import ContactForm, PhoneNumberForm

from .forms import PhoneNumberFormSet  # Already defined properly using inlineformset_factory

@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        formset = PhoneNumberFormSet(request.POST, instance=contact)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "✅ Contact updated successfully!")
            return redirect('list_contacts')
        
        if request.POST.get('delete_image') and contact.image:
            contact.image.delete()
            contact.image = None
    else:
        form = ContactForm(instance=contact)
        formset = PhoneNumberFormSet(instance=contact)

    return render(request, 'contacts/contact_form.html', {
        'form': form,
        'formset': formset,
        'empty_form': formset.empty_form,
        'home_button': True
    })





# DELETE CONTACT VIEW (Protected)
@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    if request.method == 'POST':
        contact.delete()
        return redirect('list_contacts')

    # Pass 'home_button' as True for Delete Contact page
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact, 'home_button': True})


@login_required
def bulk_delete_contacts(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_contacts')
        if selected_ids:
            Contact.objects.filter(id__in=selected_ids, user=request.user).delete()
            messages.success(request, f"{len(selected_ids)} contact(s) deleted successfully.")
        else:
            messages.warning(request, "No contacts selected.")
    return redirect('list_contacts')