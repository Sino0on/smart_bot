# Generated by Django 4.0.5 on 2022-07-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_rename_account_applicationmet_account_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/courses/'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/meeting/'),
        ),
    ]