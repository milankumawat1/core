# Generated by Django 5.2.1 on 2025-05-12 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0003_recipie_recipie_views'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipie',
            old_name='recipie_views',
            new_name='recipie_view_count',
        ),
    ]
