from django.core.management.base import BaseCommand
from bots.fill_out_appointment_bot import FillOutAppointmentBot

class Command(BaseCommand):
    help = 'Start vfs creator bot'

    def handle(self, *args, **options):
        #Example Data of Person:
        person = {
            #personality
            "FIRST_NAME": "Joe",
            "LAST_NAME": "Baidenn",
            "GENDER": "Male",
            "DATE_OF_BIRTH": "05061997", #without separetors
            "CITIZIENSHIP": "Kyrgyzstan",
            "PASSPORT_NUMBER": '20506200414356',
            "Passport_Expirty_Date": '20082030', #without separetors
            "PHONE_CODE": '996',
            "PHONE_NUMBER": '0559055934',
            "EMAIL":'gmail@gmail.com',

            #cart info
            "cart_num": '4123123123123',
            "expiry_month": 1,
            "expiry_year": 24,
            "cvv": 111,
            "name_and_surname": "Joe Baidenn",
            "address": "Pushkin\'s stree...)",
            "city_district_postcode": "Moscow, Lublino disctrict, 000000",
            
            #free appointment window
            "FREE_WINDOW": 30,
            "VISA_CENTRE": "Poland Visa Application Centre - Ankara",
        }

        ap = FillOutAppointmentBot(
            email='dr.derekwerner5036@outlook.com',
            password='bBc2CUQuu!4R',
            person=person,
            use_proxy=False,
        )
        ap.work()

    def add_arguments(self, parser) -> None:
        parser.add_argument (
            '--applicant_id',
            default=None,
            required=True,
            type=int,
            help='Start vfs creator bot',
        )