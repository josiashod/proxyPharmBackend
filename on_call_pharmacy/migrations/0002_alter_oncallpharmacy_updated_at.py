# Generated by Django 3.2.7 on 2021-09-26 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('on_call_pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oncallpharmacy',
            name='updated_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
