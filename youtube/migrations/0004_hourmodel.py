# Generated by Django 4.2.1 on 2023-05-29 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0003_delete_daymodel_delete_hourmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all', models.CharField(blank=True, max_length=700, null=True)),
            ],
        ),
    ]
