# Generated by Django 5.0.6 on 2024-09-27 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0032_alter_login_usertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregister',
            name='amountpaid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='userregister',
            name='howmuchperuser',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
