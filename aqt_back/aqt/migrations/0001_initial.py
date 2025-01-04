# Generated by Django 4.2.16 on 2024-11-08 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('LocationID', models.AutoField(primary_key=True, serialize=False)),
                ('LocationName', models.CharField(max_length=200)),
                ('Longitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('Latitude', models.DecimalField(decimal_places=6, max_digits=10)),
            ],
        ),
    ]