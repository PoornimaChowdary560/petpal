# Generated by Django 5.1.5 on 2025-05-26 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petzeno', '0012_alter_pet_species'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuccessStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(max_length=100)),
                ('owner_name', models.CharField(max_length=100)),
                ('story', models.TextField()),
                ('image', models.ImageField(default='default_pet.jpg', upload_to='pet_photos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
