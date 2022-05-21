from enum import Enum

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models

from bots.support_funcs import send_request_to_aws_lambda, start_create_applicant_account_bot
from config.settings import DEBUG

class CrawlTypes(Enum):
    EMAIL = 0
    VFS_ACCOUNT = 1
    APPOINTMENT = 2

visa_centres_type = (
    ("0", "None"),
    ("Poland Visa Application Center - Ankara", "Ankara"),
    ("Poland Visa Application Center-Antalya", "Antalya"),
    ("Poland Visa Application Center-Beyoglu", "Beyoglu"),
    ("Poland Visa Application Center-Gaziantep", "Gaziantep"),
    ("Poland Visa Application Center-Izmir", "Izmir"),
    ("Poland Visa Application Center-Trabzon", "Trabzon")
)

SUBCATEGORIES = (
    ('1- Higher Education / Yuksek Ogrenim / studia wyzsze', '1- Higher Education'),
    ('2- Turkish citizens - work permit / TC vatandaslari - calisma Izni / obywatele Turcji - w celu wykonywania pracy', '2- Turkish citizens'),
    ('3- Foreigners - work permit/ Yabanci vatandaslar - calisma Izni / cudzoziemcy - w celu wykonywania pracy', '3- Foreigners'),
    ('4- Long-Stay others / Diger Uzun Donem / wiza typu D w celu innym niz wymienione', '4- Long-Stay others')
)

class Card(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    number = models.CharField(verbose_name='Card number', max_length=18)
    code = models.CharField(verbose_name='CCV', max_length=3)
    valid_through = models.DateField(verbose_name='Valid through')
    phone_number = models.CharField(verbose_name="Phone nubmer", max_length=25)
    is_busy = models.BooleanField(verbose_name='Is busy card', default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Credit card'
        verbose_name_plural = 'Credit cards' 

class VFSAccount(models.Model):
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modified at')
    modified_by = models.DateTimeField(verbose_name='Modified by')

    username = models.CharField(verbose_name='Username', max_length=100)
    password = models.CharField(verbose_name='Password', max_length=100)

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'VFS account'
        verbose_name_plural = 'VFS accounts'

class Applicant(models.Model):
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modified at')
    modified_by = models.DateTimeField(verbose_name='Modified by')

    firstname = models.CharField(verbose_name='First name', max_length=100)
    lastname = models.CharField(verbose_name='Last name', max_length=100)
    gender = models.CharField(verbose_name='Gender', max_length=10)
    date_of_birth = models.DateField(verbose_name='Date of birth')
    citizenship = models.CharField(verbose_name='Citizenship', max_length=100)
    phone_code = models.CharField(verbose_name="Phone code", max_length=4)
    contact_number = models.CharField(verbose_name='Phone number', max_length=14)
    passport = models.CharField(verbose_name='Personal number of passport', unique=True, max_length=20)
    passport_expiry_date = models.DateField(verbose_name='Passport expiry date')
    email = models.EmailField(unique=True, blank=True, null=True)
    email_password = models.CharField(max_length=255, blank=True, null=True)

    visa_centre = models.CharField(max_length=255, choices=visa_centres_type, default="0")
    subcategory = models.CharField(max_length=255, choices=SUBCATEGORIES)

    settlement = models.ForeignKey('Settlement', verbose_name='To settlement', 
                                on_delete=models.CASCADE, blank=True, null=True)
    vfs_account = models.OneToOneField(VFSAccount, on_delete=models.CASCADE,
                                        blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'

class Appointment(models.Model):
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modified at')
    modified_by = models.DateTimeField(verbose_name='Modified by')
    
    is_success = models.BooleanField(verbose_name='Is success')
    applicant = models.ForeignKey(Applicant, verbose_name='To applicant', on_delete=models.CASCADE)
    center_name = models.CharField(verbose_name='Name of center', max_length=100) 
    date_and_time = models.DateTimeField(verbose_name='Appointment time')

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

class CrawlAttempt(models.Model):
    crawl_type = models.CharField(
        verbose_name='Crawl to', max_length=25, 
        choices=[
            (tag, tag.value) for tag in CrawlTypes]
            )
    modified_at = models.DateTimeField(verbose_name='Modified at')
    modified_by = models.DateTimeField(verbose_name='Modified by')
    applicant = models.ForeignKey(Applicant, verbose_name='To applicant', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.applicant.firstname}'

    class Meta:
        verbose_name = 'Crawl attempt'
        verbose_name_plural = 'Crawl attempts'

class Settlement(models.Model):
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modified at')
    modified_by = models.DateTimeField(verbose_name='Modified by')
    
    amount = models.PositiveIntegerField(verbose_name='Amount')

    class Meta:
        verbose_name = 'Settlement'
        verbose_name_plural = 'Settlements'

class Queue(models.Model):
    applicant_id = models.CharField(verbose_name="Applicant id number", max_length=255)
    card_id =  models.CharField(verbose_name="Card id number", max_length=255)
    sms_code = models.CharField(verbose_name="Sms code", max_length=255, blank=True, null=True)
    is_processed = models.BooleanField(verbose_name='Is processed', default=False)

    def __str__(self) -> str:
        return f"Queue of {self.applicant_id} applicant"

@receiver(post_save, sender=Applicant)
def create_applicant_account_signal(sender, instance, created, *args, **kwargs):
    """Wakes up the lambda function"""
    
    if DEBUG:
        start_create_applicant_account_bot(instance.id)

    send_request_to_aws_lambda()