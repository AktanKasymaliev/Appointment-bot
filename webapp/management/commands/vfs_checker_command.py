from django.core.management.base import BaseCommand
from bots.support_funcs import send_request_to_get_all_applicants_data_endpoint
from bots.vfs_appointment_checker_bot import VFSAppointmentCheckerBot

class Command(BaseCommand):
    help = 'Start vfs creator bot'

    def handle(self, *args, **options):
        checker = VFSAppointmentCheckerBot(
            email='dr.derekwerner5036@outlook.com',
            password='bBc2CUQuu!4R',
            use_proxy=True,
        )
        checker.work()