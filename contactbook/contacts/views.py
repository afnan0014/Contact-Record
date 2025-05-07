from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm


# Create your views here.
def contact_list(request):
    search_query = request.GET.get('search', '')  # Get search text from URL (like ?search=John)
    if search_query:
        contacts = Contact.objects.filter(name__icontains=search_query)
    else:
        contacts = Contact.objects.all()
    return render(request, 'contacts/contact_list.html', {'contacts': contacts, 'search_query': search_query})

def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')  # Go back to home page
    else:
        form = ContactForm()
    return render(request, 'contacts/contact_form.html', {'form': form})

def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_form.html', {'form': form})

def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})
