# Generated by Django 3.0.3 on 2020-03-14 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='name',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]