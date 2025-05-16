from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.list_contacts, name='list_contacts'),
    path('add/', views.add_contact, name='add_contact'),
    path('edit/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('delete/<int:pk>/', views.delete_contact, name='delete_contact'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('bulk-delete/', views.bulk_delete_contacts, name='bulk_delete_contacts'),
]

# ✅ This should be **outside** the urlpatterns list
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
