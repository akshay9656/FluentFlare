# Generated by Django 5.0.6 on 2024-09-25 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0031_remove_userregister_user_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='userType',
            field=models.CharField(choices=[('user', 'User'), ('promoter', 'Promoter')], default='user', max_length=50),
        ),
    ]
