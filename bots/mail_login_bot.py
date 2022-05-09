
from typing import Any
from bots.outlook_account_mail_checker import OutlookCheckerMailBot


class MailLoginBot(OutlookCheckerMailBot):
    URL = 'https://outlook.office.com/mail/'
    
    def work(self):
        print("=========Loginig in Outlook User\'s Mail=========")
        return super().login(), self.driver.close()

    def generate_report(self) -> Any:
        return super().generate_report()