# Generated by Django 5.0.6 on 2024-09-25 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfluentflare', '0030_paymentprice_created_at_paymentprice_payment_qrcode_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregister',
            name='user_dob',
        ),
        migrations.AddField(
            model_name='userregister',
            name='redeem_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
