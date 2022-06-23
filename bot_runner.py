import subprocess
from time import sleep

import boto3
from pyvirtualdisplay import Display

from bots.vfs_appointment_checker_bot import VFSAppointmentCheckerBot
from bots.bot_configurations import load_conf

from configparser import ConfigParser

config_parse = ConfigParser()
config_parse.read("bot_settings.ini")

BUCKET_NAME = 'botsessionrecordings'
s3_resource = boto3.resource(
    's3',
    region_name='us-east-1',
    aws_access_key_id=load_conf(config_parse, 'AWS', 'AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=load_conf(config_parse, 'AWS', 'AWS_SECRET_ACCESS_KEY')
)


def main():
    """
    This module will be used to start a bot which will be running
    without depending on Django instance.
    """
    display = Display(visible=False, extra_args=[':25'], size=(2560, 1440)) 
    display.start()
    video_filename = 'recording.mp4'
    recorder = subprocess.Popen(['/usr/bin/ffmpeg', '-f', 'x11grab', '-video_size',
                                '2560x1440', '-framerate', '25', '-probesize',
                                '10M', '-i', ':25', '-y', '/tmp/' + video_filename])
    try:
        checker = VFSAppointmentCheckerBot(
            email='dr.derekwerner5036@outlook.com',
            password='bBc2CUQuu!4R',
            use_proxy=True,
        )
        checker.work()
    except Exception as e:
        print('FAILED', e)
    finally:
        sleep(7)
        recorder.terminate()
        sleep(7)
        print('Closed recorder')
        recorder.wait(timeout=20)
        sleep(10)
        s3_file_object = s3_resource.Object(
            bucket_name=BUCKET_NAME, key='screenshot.png')
        s3_file_object.upload_file('/tmp/' + 'screenshot.png')
        s3_file_object = s3_resource.Object(
            bucket_name=BUCKET_NAME, key=video_filename)
        s3_file_object.upload_file('/tmp/' + video_filename)

if __name__ == '__main__':
    main()