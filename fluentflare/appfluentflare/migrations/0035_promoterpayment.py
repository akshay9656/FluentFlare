# Generated by Django 5.0.6 on 2024-09-29 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0034_alter_userregister_howmuchperuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promoterpayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appfluentflare.userregister')),
            ],
        ),
    ]
