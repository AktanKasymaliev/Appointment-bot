from django.core.management.base import BaseCommand

from bots import outlook_account_creator, outlook_account_mail_checker, vfs_account_creator, \
                    fill_out_appointment_bot, mail_login_bot
from webapp.support_funcs import send_request_to_add_email_password_endpoint
from webapp.support_funcs import make_person_for_bot


class Command(BaseCommand):
    help = 'Runs all bots'

    def handle(self, *args, **options):
        applicant_id = options["applicant_id"]

        outlook_mail_login_data = outlook_account_creator.OutlookAccountCreator(use_proxy=True).work()
        email = outlook_mail_login_data['email']
        password = outlook_mail_login_data['password']

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
            person=make_person_for_bot(applicant_id, email),
            use_proxy=True
        ).work()

        send_request_to_add_email_password_endpoint(
            applicant_id=applicant_id,
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