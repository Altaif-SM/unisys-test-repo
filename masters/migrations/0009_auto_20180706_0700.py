# Generated by Django 2.0.6 on 2018-07-06 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0008_auto_20180706_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developmentprogram',
            name='activity',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='developmentprogram',
            name='outcome',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='developmentprogram',
            name='remark',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
