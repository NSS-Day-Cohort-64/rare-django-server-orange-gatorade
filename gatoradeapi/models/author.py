from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    profile_image_url = models.CharField(max_length=500)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    def first_name(self):
        return self.user.first_name
    def last_name(self):
        return self.user.last_name
    def username(self):
        return self.user.username
    def created_on(self):
        return self.user.date_joined
    def is_staff(self):
        return self.user.is_staff
    def is_active(self):
        return self.user.is_active
