# Generated by Django 2.2 on 2022-01-28 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='api_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]