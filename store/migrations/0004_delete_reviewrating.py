# Generated by Django 4.0.4 on 2022-05-24 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_reviewrating_updated_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReviewRating',
        ),
    ]
