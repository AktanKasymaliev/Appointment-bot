from django.core.management.base import BaseCommand

from bots.fill_out_appointment_bot import FillOutAppointmentBot
from bots.support_funcs import get_card, intialize_bot_with_firewall_bypass, make_person_for_bot

class Command(BaseCommand):
    help = 'Start vfs filler bot'

    def handle(self, *args, **options):
        applicant_id = options["applicant_id"]
        card_data = get_card()
        email = 'dr.derekwerner5036@outlook.com'
        password = 'bBc2CUQuu!4R'
        intialize_bot_with_firewall_bypass(
            FillOutAppointmentBot,
            email=email,
            password=password,
            person=make_person_for_bot(applicant_id, email, card_data),
            use_proxy=True,
        )

    def add_arguments(self, parser) -> None:
        parser.add_argument (
            '--applicant_id',
            default=None,
            required=True,
            type=int,
            help='Start vfs creator bot',
        )