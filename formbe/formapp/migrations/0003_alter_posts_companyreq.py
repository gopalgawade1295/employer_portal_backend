# Generated by Django 5.0 on 2023-12-31 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0002_alter_company_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='companyreq',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='formapp.company'),
        ),
    ]
