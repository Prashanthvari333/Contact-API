# Generated by Django 4.2.15 on 2024-08-20 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='spam_count',
            field=models.IntegerField(default=0),
        ),
    ]
