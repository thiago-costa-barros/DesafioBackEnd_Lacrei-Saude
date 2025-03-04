# Generated by Django 5.1.6 on 2025-02-16 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0002_profession_alter_healthprofessional_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthprofessional',
            name='profession',
            field=models.ForeignKey(db_column='ProfessionId', null=True, on_delete=django.db.models.deletion.SET_NULL, to='professionals.profession'),
        ),
    ]
