from bots.vfs_appointment_checker_bot import VFSAppointmentCheckerBot

def lambda_handler(event, context):
    print('Starting bot', event)
    bot = VFSAppointmentCheckerBot(
        email='dr.derekwerner5036@outlook.com',
        password='bBc2CUQuu!4R',
        use_proxy=True
    )
    bot.work()
    print('bot stopped', event)
    return True