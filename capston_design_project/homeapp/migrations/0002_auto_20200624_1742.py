# Generated by Django 3.0.4 on 2020-06-24 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='id',
        ),
        migrations.AlterField(
            model_name='invitation',
            name='request_user',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
