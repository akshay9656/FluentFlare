# Generated by Django 5.0.6 on 2024-08-15 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0024_alter_userregister_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregister',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]