# Generated by Django 2.2 on 2020-10-04 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20201002_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='payment_mode',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
    ]
