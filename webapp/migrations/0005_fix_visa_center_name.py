# Generated by Django 4.0.4 on 2022-07-14 09:47

from django.db import migrations


class Migration(migrations.Migration):

    def fix_visa_center_name(apps, schema_editor):
        Applicant = apps.get_model('webapp', 'Applicant')
        beyoglu_applicants = Applicant.objects.filter(visa_centre='Poland Visa Application Center-Istanbul (Beyoglu)')
        Applicant.objects.bulk_update(
            [
                Applicant(id=app.id, visa_centre='Poland Visa Application Center - Istanbul (Beyoglu)')
                for app in beyoglu_applicants
            ],
            ['visa_centre'],
            batch_size=1000
        )

    dependencies = [
        ('webapp', '0004_alter_applicant_visa_centre'),
    ]

    operations = [
        migrations.RunPython(fix_visa_center_name)
    ]
