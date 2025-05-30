# Generated by Django 5.2.1 on 2025-05-12 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0008_delete_subjectmarksold'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentmarks', to='vege.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vege.subject')),
            ],
            options={
                'unique_together': {('student', 'subject')},
            },
        ),
    ]
