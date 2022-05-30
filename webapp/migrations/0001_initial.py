# Generated by Django 4.0.4 on 2022-05-23 07:17

from django.db import migrations, models
import django.db.models.deletion
import webapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(verbose_name='Modified at')),
                ('modified_by', models.DateTimeField(verbose_name='Modified by')),
                ('firstname', models.CharField(max_length=100, verbose_name='First name')),
                ('lastname', models.CharField(max_length=100, verbose_name='Last name')),
                ('gender', models.CharField(max_length=10, verbose_name='Gender')),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('citizenship', models.CharField(max_length=100, verbose_name='Citizenship')),
                ('phone_code', models.CharField(max_length=4, verbose_name='Phone code')),
                ('contact_number', models.CharField(max_length=14, verbose_name='Phone number')),
                ('passport', models.CharField(max_length=20, unique=True, verbose_name='Personal number of passport')),
                ('passport_expiry_date', models.DateField(verbose_name='Passport expiry date')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('email_password', models.CharField(blank=True, max_length=255, null=True)),
                ('is_success', models.BooleanField(default=False, verbose_name='Is success')),
                ('is_busy', models.BooleanField(default=False, verbose_name='Is busy')),
                ('visa_centre', models.CharField(choices=[('0', 'None'), ('Poland Visa Application Center - Ankara', 'Ankara'), ('Poland Visa Application Center-Antalya', 'Antalya'), ('Poland Visa Application Center-Beyoglu', 'Beyoglu'), ('Poland Visa Application Center-Gaziantep', 'Gaziantep'), ('Poland Visa Application Center-Izmir', 'Izmir'), ('Poland Visa Application Center-Trabzon', 'Trabzon')], default='0', max_length=255)),
                ('subcategory', models.CharField(choices=[('1- Higher Education / Yuksek Ogrenim / studia wyzsze', '1- Higher Education'), ('2- Turkish citizens - work permit / TC vatandaslari - calisma Izni / obywatele Turcji - w celu wykonywania pracy', '2- Turkish citizens'), ('3- Foreigners - work permit/ Yabanci vatandaslar - calisma Izni / cudzoziemcy - w celu wykonywania pracy', '3- Foreigners'), ('4- Long-Stay others / Diger Uzun Donem / wiza typu D w celu innym niz wymienione', '4- Long-Stay others')], max_length=255)),
            ],
            options={
                'verbose_name': 'Applicant',
                'verbose_name_plural': 'Applicants',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('number', models.CharField(max_length=18, verbose_name='Card number')),
                ('code', models.CharField(max_length=3, verbose_name='CCV')),
                ('valid_through', models.DateField(verbose_name='Valid through')),
                ('phone_number', models.CharField(max_length=25, verbose_name='Phone nubmer')),
                ('is_busy', models.BooleanField(default=False, verbose_name='Is busy card')),
            ],
            options={
                'verbose_name': 'Credit card',
                'verbose_name_plural': 'Credit cards',
            },
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_id', models.CharField(max_length=255, verbose_name='Applicant id number')),
                ('card_id', models.CharField(max_length=255, verbose_name='Card id number')),
                ('sms_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Sms code')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Is processed')),
            ],
        ),
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(verbose_name='Modified at')),
                ('modified_by', models.DateTimeField(verbose_name='Modified by')),
                ('amount', models.PositiveIntegerField(verbose_name='Amount')),
            ],
            options={
                'verbose_name': 'Settlement',
                'verbose_name_plural': 'Settlements',
            },
        ),
        migrations.CreateModel(
            name='VFSAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(verbose_name='Modified at')),
                ('modified_by', models.DateTimeField(verbose_name='Modified by')),
                ('username', models.CharField(max_length=100, verbose_name='Username')),
                ('password', models.CharField(max_length=100, verbose_name='Password')),
            ],
            options={
                'verbose_name': 'VFS account',
                'verbose_name_plural': 'VFS accounts',
            },
        ),
        migrations.CreateModel(
            name='CrawlAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crawl_type', models.CharField(choices=[(webapp.models.CrawlTypes['EMAIL'], 0), (webapp.models.CrawlTypes['VFS_ACCOUNT'], 1), (webapp.models.CrawlTypes['APPOINTMENT'], 2)], max_length=25, verbose_name='Crawl to')),
                ('modified_at', models.DateTimeField(verbose_name='Modified at')),
                ('modified_by', models.DateTimeField(verbose_name='Modified by')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.applicant', verbose_name='To applicant')),
            ],
            options={
                'verbose_name': 'Crawl attempt',
                'verbose_name_plural': 'Crawl attempts',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(verbose_name='Modified at')),
                ('modified_by', models.DateTimeField(verbose_name='Modified by')),
                ('is_success', models.BooleanField(verbose_name='Is success')),
                ('center_name', models.CharField(max_length=100, verbose_name='Name of center')),
                ('date_and_time', models.DateTimeField(verbose_name='Appointment time')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.applicant', verbose_name='To applicant')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
            },
        ),
        migrations.AddField(
            model_name='applicant',
            name='settlement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.settlement', verbose_name='To settlement'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='vfs_account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.vfsaccount'),
        ),
    ]
