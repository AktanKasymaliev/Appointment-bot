from django.core.management.base import BaseCommand
from bots.vfs_account_login import VFSLoginBot

class Command(BaseCommand):
    help = 'Start email creator bot'

    def handle(self, *args, **options):
        # Proxies.load_proxies('proxies.txt')
        bot = VFSLoginBot(
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