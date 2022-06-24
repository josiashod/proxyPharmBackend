# Generated by Django 3.2.7 on 2021-12-06 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0003_auto_20211126_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacy',
            name='drugs',
            field=models.ManyToManyField(through='pharmacy.PharmacyDrug', to='pharmacy.Drug'),
        ),
    ]