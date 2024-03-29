from django.core.management.base import BaseCommand

from bots.vfs_appointment_checker_bot import VFSAppointmentCheckerBot
from bots.support_funcs import intialize_bot_with_firewall_bypass

class Command(BaseCommand):
    help = 'Start vfs creator bot'

    def handle(self, *args, **options):

        intialize_bot_with_firewall_bypass(
            VFSAppointmentCheckerBot,
            use_proxy=True,
        )