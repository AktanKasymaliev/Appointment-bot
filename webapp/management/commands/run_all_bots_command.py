from django.core.management.base import BaseCommand
from bots import outlook_account_creator, outlook_account_mail_checker, vfs_account_creator, \
                    vfs_account_login, mail_login_bot

class Command(BaseCommand):
    help = 'Runs all bots'

    def handle(self, *args, **options):
        print('=========Creating new Outlook email account=========')
        outlook_mail = outlook_account_creator.OutlookAccountCreator(use_proxy=True).work()
        email = outlook_mail['email']
        password = outlook_mail['password']

        print("=========Loginig in Outlook User\'s Mail=========")
        mail_login_bot.MailLoginBot(
            email=email,
            password=password,
            use_proxy=True
        ).work()
        

        print("=========Creating VFS User=========")
        vfs_account_creator.VFSAccountCreate(
            email=email,
            password=password,
            use_proxy=True
            ).work()

        print("=========Checking Outlook User\'s Mail=========")
        outlook_account_mail_checker.OutlookCheckerMailBot(
            email=email,
            password=password,
            use_proxy=True
            ).work()