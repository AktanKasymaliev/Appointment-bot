from django.core.management.base import BaseCommand

from bots.support_funcs import intialize_bot_with_firewall_bypass
from bots.outlook_account_creator import OutlookAccountCreator

class Command(BaseCommand):
    help = 'Start email creator bot'

    def handle(self, *args, **options):
        intialize_bot_with_firewall_bypass(
            OutlookAccountCreator,
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