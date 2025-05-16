from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='contact_images/', blank=True, null=True)  # ✅ New field

    def __str__(self):
        return self.name

class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact, related_name='phone_numbers', on_delete=models.CASCADE)
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number
