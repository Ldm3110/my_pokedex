# Generated by Django 3.2.12 on 2023-01-11 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0002_rename_surname_pokemon_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('img_uri', models.URLField()),
                ('description', models.TextField(max_length=250)),
            ],
        ),
    ]
