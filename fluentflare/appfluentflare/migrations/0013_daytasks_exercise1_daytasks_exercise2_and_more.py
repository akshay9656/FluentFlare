# Generated by Django 5.0.6 on 2024-08-10 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0012_remove_usermessage_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='daytasks',
            name='exercise1',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='daytasks',
            name='exercise2',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='daytasks',
            name='exercise3',
            field=models.TextField(null=True),
        ),
    ]