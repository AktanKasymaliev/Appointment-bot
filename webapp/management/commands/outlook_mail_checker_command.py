from django.core.management.base import BaseCommand

from bots.outlook_account_mail_checker import OutlookCheckerMailBot
from bots.support_funcs import intialize_bot_with_firewall_bypass


class Command(BaseCommand):
    help = 'Start email checker bot'

    def handle(self, *args, **options):
        intialize_bot_with_firewall_bypass(
            OutlookCheckerMailBot,
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
            help='Start mail checker bot',
        )