# Generated by Django 5.0.1 on 2024-02-09 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='hashcode',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
    ]
