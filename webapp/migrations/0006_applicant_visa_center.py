# Generated by Django 4.0.4 on 2022-05-20 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_card_is_busy'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='visa_center',
            field=models.CharField(choices=[('0', 'None'), ('1', 'Poland Visa Application Center - Ankara'), ('2', 'Poland Visa Application Center-Antalya'), ('3', 'Poland Visa Application Center-Beyoglu'), ('4', 'Poland Visa Application Center-Gaziantep'), ('5', 'Poland Visa Application Center-Izmir'), ('6', 'Poland Visa Application Center-Trabzon')], default='0', max_length=255),
        ),
    ]
