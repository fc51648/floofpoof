# Generated by Django 3.0.3 on 2020-05-29 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_auto_20200528_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(blank=True, max_length=4, null=True, unique=True),
        ),
    ]
