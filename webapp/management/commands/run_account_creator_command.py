from django.core.management.base import BaseCommand

from bots import outlook_account_creator, outlook_account_mail_checker, vfs_account_creator, \
                    fill_out_appointment_bot, mail_login_bot
from webapp.models import Applicant
from webapp.support_funcs import send_request_to_endpoint
from webapp.support_funcs import make_person_for_bot


class Command(BaseCommand):
    help = 'Runs all bots'

    def handle(self, *args, **options):
        applicant = Applicant.objects.get(options['applicant_id'])
        outlook_mail = outlook_account_creator.OutlookAccountCreator(use_proxy=True).work()
        email = outlook_mail['email']
        password = outlook_mail['password']

        mail_login_bot.MailLoginBot(
            email=email,
            password=password,
            use_proxy=True
        ).work()
        
        vfs_account_creator.VFSAccountCreate(
            email=email,
            password=password,
            use_proxy=True
            ).work()

        outlook_account_mail_checker.OutlookCheckerMailBot(
            email=email,
            password=password,
            use_proxy=True
            ).work()
        
        fill_out_appointment_bot.FillOutAppointmentBot(
            email=email,
            password=password,
            person=make_person_for_bot(applicant, email),
            use_proxy=True
        ).work()

        send_request_to_endpoint(
            applicant_id=options["applicant_id"],
            email=email,
            password=password
        )

    def add_arguments(self, parser) -> None:
        parser.add_argument (
            '--applicant_id',
            default=None,
            required=True,
            type=int,
            help='Start account creator bot',
        )