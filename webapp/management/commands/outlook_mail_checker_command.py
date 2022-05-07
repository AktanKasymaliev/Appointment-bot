from bots.outlook_account_mail_checker import OutlookCheckerMailBot
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start email creator bot'

    def handle(self, *args, **options):
        # Proxies.load_proxies('proxies.txt')
        bot = OutlookCheckerMailBot(
            email='outlook@outlook.com',
            password='password',
            use_proxy=False
            )
        bot.work()

    def add_arguments(self, parser) -> None:
        parser.add_argument (
            '--applicant_id',
            default=None,
            required=True,
            type=int,
            help='Start vfs creator bot',
        )