# Generated by Django 4.1.1 on 2022-10-07 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdata',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.location'),
        ),
        migrations.AlterUniqueTogether(
            name='weatherdata',
            unique_together={('location', 'data', 'date')},
        ),
    ]
