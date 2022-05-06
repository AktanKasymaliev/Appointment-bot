from django.core.management.base import BaseCommand
from bots.bot_managing import Proxies
from bots.outlook_account_creator import OutlookAccountCreator

class Command(BaseCommand):
    help = 'Start email creator bot'

    def handle(self, *args, **options):
        Proxies.load_proxies('proxies.txt')
        bot = OutlookAccountCreator(use_proxy=True)
        bot.work()

    def add_arguments(self, parser) -> None:
        parser.add_argument (
            '--applicant_id',
            default=None,
            required=True,
            type=int,
            help='Start email creator bot',
        )