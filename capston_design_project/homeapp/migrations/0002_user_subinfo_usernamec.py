# Generated by Django 3.0.4 on 2020-05-01 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_subinfo',
            name='usernameC',
            field=models.CharField(max_length=30, null=True),
        ),
    ]