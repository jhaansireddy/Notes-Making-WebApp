from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200,default="Untitled")
    content = models.CharField(max_length=10000)
    tags = models.ManyToManyField(Tag)
    user = models.ManyToManyField(User)
    createdon = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title