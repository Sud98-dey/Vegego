# Generated by Django 2.2 on 2020-11-13 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20201113_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_name',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='Product_M',
        ),
    ]
