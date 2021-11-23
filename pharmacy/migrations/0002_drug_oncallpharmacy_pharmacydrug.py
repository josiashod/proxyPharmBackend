# Generated by Django 3.2.7 on 2021-11-23 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('dose', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('chemical_composition', models.CharField(blank=True, max_length=255, null=True)),
                ('class_of_drug', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PharmacyDrug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pharmacy.drug')),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pharmacy.pharmacy')),
            ],
        ),
        migrations.CreateModel(
            name='OnCallPharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateField()),
                ('end_at', models.DateField()),
                ('start_hour', models.TimeField()),
                ('end_hour', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pharmacy.pharmacy')),
            ],
        ),
    ]
