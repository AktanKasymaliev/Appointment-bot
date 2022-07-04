from django.core.management.base import BaseCommand

from bots.support_funcs import intialisate_bot_with_firewall_bypass
from bots.mail_login_bot import MailLoginBot

class Command(BaseCommand):
    help = 'Start email creator bot'

    def handle(self, *args, **options):
        intialisate_bot_with_firewall_bypass(
            MailLoginBot,
            email='outlook@outlook.com',
            password='password1234',
            use_proxy=True
        )

    def add_arguments(self, parser) -> None:
        parser.add_argument (
            '--applicant_id',
            default=None,
            required=True,
            type=int,
            help='Start email creator bot',
        )