# Generated by Django 4.2.15 on 2024-08-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spam', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spamreport',
            old_name='timestamp',
            new_name='report_date',
        ),
        migrations.AddField(
            model_name='spamreport',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
