# Generated by Django 4.0.3 on 2022-06-19 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesapp', '0002_note_createdon_note_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(default='Untitled', max_length=200),
        ),
    ]