# Generated by Django 5.1.9 on 2025-05-13 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0014_alter_reportcard_date_of_report_card_generation'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
