# Generated by Django 5.0.6 on 2024-08-06 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0008_progressbar'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressbar',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appfluentflare.userregister'),
        ),
    ]
