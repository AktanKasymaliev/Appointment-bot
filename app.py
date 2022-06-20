from bots.vfs_appointment_checker_bot import VFSAppointmentCheckerBot

def main():
    checker = VFSAppointmentCheckerBot(
        email='dr.derekwerner5036@outlook.com',
        password='bBc2CUQuu!4R',
        use_proxy=True,
    )
    checker.work()

if __name__ == '__main__':
    main()