# Generated by Django 4.0.2 on 2022-02-24 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(max_length=200)),
                ('startTime', models.DateTimeField(verbose_name='start time')),
                ('endTime', models.DateTimeField(verbose_name='end time')),
            ],
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('z', models.IntegerField()),
                ('t', models.DateTimeField(verbose_name='timestamp')),
                ('quality', models.IntegerField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exhibitionInferenceApp.session')),
            ],
        ),
    ]
