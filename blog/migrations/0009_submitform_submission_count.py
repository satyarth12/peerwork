# Generated by Django 2.2.6 on 2020-09-21 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_submitform_granted'),
    ]

    operations = [
        migrations.AddField(
            model_name='submitform',
            name='submission_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]