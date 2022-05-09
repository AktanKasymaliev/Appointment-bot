from django.core.management.base import BaseCommand
from bots import outlook_account_creator, outlook_account_mail_checker, vfs_account_creator, \
                    vfs_account_login, mail_login_bot

class Command(BaseCommand):
    help = 'Runs all bots'

    def handle(self, *args, **options):
        outlook_mail = outlook_account_creator.OutlookAccountCreator(use_proxy=True).work()
        email = outlook_mail['email']
        password = outlook_mail['password']

        mail_login_bot.MailLoginBot(
            email=email,
            password=password,
            use_proxy=True
        ).work()

        vfs_account_creator.VFSAccountCreate(
            email=email,
            password=password,
            use_proxy=True
            ).work()
            
        outlook_account_mail_checker.OutlookCheckerMailBot(
            email=email,
            password=password,
            use_proxy=True
            ).work()