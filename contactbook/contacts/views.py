from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contact
from .forms import ContactForm


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


# HOME / CONTACT LIST VIEW (Protected)
@login_required
def list_contacts(request):
    search_query = request.GET.get('search', '')
    contacts = Contact.objects.filter(user=request.user)

    if search_query:
        contacts = contacts.filter(name__icontains=search_query)

    return render(request, 'contacts/contact_list.html', {
        'contacts': contacts,
        'search_query': search_query
    })


# ADD CONTACT VIEW (Protected)
@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user   # Assign logged-in user
            contact.save()
            return redirect('list_contacts')
    else:
        form = ContactForm()

    # Pass 'home_button' as True for Add Contact page
    return render(request, 'contacts/contact_form.html', {'form': form, 'home_button': True})


# EDIT CONTACT VIEW (Protected)
@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('list_contacts')
    else:
        form = ContactForm(instance=contact)

    # Pass 'home_button' as True for Edit Contact page
    return render(request, 'contacts/contact_form.html', {'form': form, 'home_button': True})


# DELETE CONTACT VIEW (Protected)
@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    if request.method == 'POST':
        contact.delete()
        return redirect('list_contacts')

    # Pass 'home_button' as True for Delete Contact page
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact, 'home_button': True})
