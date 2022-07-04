from django.core.management.base import BaseCommand

from bots.vfs_appointment_checker_bot import VFSAppointmentCheckerBot
from bots.support_funcs import intialisate_bot_with_firewall_bypass

class Command(BaseCommand):
    help = 'Start vfs creator bot'

    def handle(self, *args, **options):

        intialisate_bot_with_firewall_bypass(
            VFSAppointmentCheckerBot,
            email='dr.derekwerner5036@outlook.com',
            password='bBc2CUQuu!4R',
            use_proxy=True,
        )