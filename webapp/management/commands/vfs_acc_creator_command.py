from django.core.management.base import BaseCommand
from bots.vfs_account_creator import VFSAccountCreate

class Command(BaseCommand):
    help = 'Start email creator bot'

    def handle(self, *args, **options):
        # Proxies.load_proxies('proxies.txt')
        vfs_bot = VFSAccountCreate(
            email='outlook@outlook.com',
            password='password1234',
            use_proxy=False
            )
        vfs_bot.work()

    def add_arguments(self, parser) -> None:
        parser.add_argument (
            '--applicant_id',
            default=None,
            required=True,
            type=int,
            help='Start vfs creator bot',
        )