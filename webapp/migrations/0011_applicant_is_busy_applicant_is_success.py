# Generated by Django 4.0.4 on 2022-05-22 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_applicant_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='is_busy',
            field=models.BooleanField(default=False, verbose_name='Is busy'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='is_success',
            field=models.BooleanField(default=False, verbose_name='Is success'),
        ),
    ]
