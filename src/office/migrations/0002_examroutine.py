# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-03 09:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_subject'),
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamRoutine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('start_hour', models.TimeField(blank=True, null=True)),
                ('end_hour', models.TimeField(blank=True, null=True)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Class')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.School')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Subject')),
            ],
        ),
    ]
