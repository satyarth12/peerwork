# Generated by Django 2.2.6 on 2020-09-25 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200921_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', max_length=200, unique=True),
        ),
    ]
