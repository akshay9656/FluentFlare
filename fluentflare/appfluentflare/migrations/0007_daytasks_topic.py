# Generated by Django 5.0.6 on 2024-08-06 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0006_userregister_enrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='daytasks',
            name='topic',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
