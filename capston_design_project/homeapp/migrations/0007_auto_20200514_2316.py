# Generated by Django 3.0.4 on 2020-05-14 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0006_auto_20200514_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qrcode_info',
            old_name='qrcode_image',
            new_name='image',
        ),
    ]
