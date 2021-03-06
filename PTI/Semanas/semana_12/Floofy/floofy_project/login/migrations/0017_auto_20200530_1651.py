# Generated by Django 3.0.3 on 2020-05-30 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_meeting_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='blocks',
            field=models.ManyToManyField(blank=True, to='login.Block'),
        ),
        migrations.AlterField(
            model_name='user',
            name='degree',
            field=models.ManyToManyField(blank=True, to='login.Degree'),
        ),
        migrations.AlterField(
            model_name='user',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='login.Subject'),
        ),
    ]
