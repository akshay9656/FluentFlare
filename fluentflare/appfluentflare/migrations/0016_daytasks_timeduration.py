# Generated by Django 5.0.6 on 2024-08-10 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0015_daytasks_exercise1ans_daytasks_exercise2ans_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='daytasks',
            name='timeduration',
            field=models.TextField(null=True),
        ),
    ]