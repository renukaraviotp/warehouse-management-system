# Generated by Django 4.2.6 on 2023-11-25 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouseapp', '0013_alter_client_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='photo',
            field=models.FileField(null=True, upload_to='image/'),
        ),
    ]
