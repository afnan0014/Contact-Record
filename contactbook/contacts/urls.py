from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_list, name='contact_list'),  # Home page, shows all contacts
    path('add/', views.add_contact, name='add_contact'),  # Page to add a new contact
    path('edit/<int:pk>/', views.edit_contact, name='edit_contact'),  # Page to edit a contact
    path('delete/<int:pk>/', views.delete_contact, name='delete_contact'),  # Page to delete a contact
]
