# Generated by Django 4.0.2 on 2022-03-09 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitionInferenceApp', '0007_remove_device_id_alter_device_hardwareid_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reading',
            options={'permissions': [('visualise_reading', 'Can view visualisation pages')]},
        ),
    ]
