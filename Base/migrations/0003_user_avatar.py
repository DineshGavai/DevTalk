# Generated by Django 5.0.6 on 2024-06-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]
