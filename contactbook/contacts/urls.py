from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_contacts, name='list_contacts'),
    path('add/', views.add_contact, name='add_contact'),
    path('edit/<int:pk>/', views.edit_contact, name='edit_contact'),  # Change id to pk
    path('delete/<int:pk>/', views.delete_contact, name='delete_contact'),  # Change id to pk
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

