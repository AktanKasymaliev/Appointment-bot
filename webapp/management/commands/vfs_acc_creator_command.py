from django.core.management.base import BaseCommand
from bots.bot_managing import Proxies
from bots.vfs_account_creator import VFSAccountCreate

class Command(BaseCommand):
    help = 'Start email creator bot'

    def handle(self, *args, **options):
        # Proxies.load_proxies('proxies.txt')
        bot = VFSAccountCreate(use_proxy=False)
        bot.work()

    def add_arguments(self, parser) -> None:
        parser.add_argument (
            '--applicant_id',
            default=None,
            required=True,
            type=int,
            help='Start vfs creator bot',
        )