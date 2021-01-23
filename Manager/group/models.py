from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
# from accounts.models import User


from group.generate import ran_code
from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()



class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    code = models.CharField(max_length=8)
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(User,through="GroupMember")
    creator = models.CharField(max_length=255)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.code = ran_code(8)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("group:class_single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name="memberships",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("group", "user")
