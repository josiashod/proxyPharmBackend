# Generated by Django 3.2.7 on 2021-10-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.FileField(default=None, upload_to='')),
                ('thumbnail_image', models.FileField(default=None, upload_to='')),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('website', models.URLField(max_length=255)),
                ('longitude', models.FloatField(unique=True)),
                ('latitude', models.FloatField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
            ],
        ),
    ]
