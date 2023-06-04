from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class CustomUser(AbstractUser):
    gender = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    pseudonymous_name = models.CharField(max_length=255, blank=True, null=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    def calculate_age(self):
        if self.dob:
            today = datetime.date.today()
            age = today.year - self.dob.year
            if today.month < self.dob.month or (today.month == self.dob.month and today.day < self.dob.day):
                age -= 1
            return age
        return None