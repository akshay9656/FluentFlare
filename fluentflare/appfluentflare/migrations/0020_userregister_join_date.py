# Generated by Django 5.0.6 on 2024-08-15 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0019_userregister_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregister',
            name='join_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]