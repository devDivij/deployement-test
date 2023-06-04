from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CustomUser = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ImageSet(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image_sets/', default='default_image.jpg', null=True)
    color1 = models.CharField(max_length=50, null=True)
    color2 = models.CharField(max_length=50, null=True)
    color3 = models.CharField(max_length=50, null=True)
    color4 = models.CharField(max_length=50, null=True)
    color5 = models.CharField(max_length=50, null=True)
    color6 = models.CharField(max_length=50, null=True)
    color7 = models.CharField(max_length=50, null=True)
    color8 = models.CharField(max_length=50, null=True)
    color9 = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Decision(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    is_daily_decision = models.BooleanField(default=False)
    is_quick_decision = models.BooleanField(default=False)
    is_public_decision = models.BooleanField(default=False)
    image_set = models.ForeignKey(ImageSet, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    situation = models.TextField(max_length=255, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        if self.title:
            return self.title.strip()
        return "Untitled Decision"

class Option(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    content = models.TextField(max_length=20)
    is_preferred = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Vote(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    message = models.TextField(max_length=255, null=True, blank=True)
    pros = models.TextField(max_length=255, null=True, blank=True)
    cons = models.TextField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote for {self.option.content}"