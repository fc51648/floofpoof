# Generated by Django 3.0.3 on 2020-05-30 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_auto_20200530_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
