from django.core.management.base import BaseCommand
from bots.vfs_appointment_checker_bot import VFSAppointmentCheckerBot

class Command(BaseCommand):
    help = 'Start vfs creator bot'

    def handle(self, *args, **options):
        checker = VFSAppointmentCheckerBot(
            email='dr.derekwerner5036@outlook.com',
            password='bBc2CUQuu!4R',
            use_proxy=False,
        )
        checker.work()