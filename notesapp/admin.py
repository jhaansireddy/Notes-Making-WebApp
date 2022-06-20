from django.contrib import admin
from notesapp.models import Tag, Note

# Register your models here.
admin.site.register(Tag)

admin.site.register(Note)