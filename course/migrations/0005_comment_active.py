# Generated by Django 4.1.1 on 2023-04-25 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]