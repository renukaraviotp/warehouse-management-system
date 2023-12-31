# Generated by Django 4.2.6 on 2023-11-25 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouseapp', '0011_remove_delivery1_email_remove_delivery1_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery1',
            name='user',
        ),
        migrations.AddField(
            model_name='delivery1',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='delivery1',
            name='first_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='delivery1',
            name='last_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='delivery1',
            name='user_type',
            field=models.CharField(default=2, max_length=10),
        ),
        migrations.AddField(
            model_name='delivery1',
            name='username',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
