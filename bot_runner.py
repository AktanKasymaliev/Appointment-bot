import subprocess
from time import sleep
from uuid import uuid4

import boto3
from pyvirtualdisplay import Display

from selenium.common.exceptions import WebDriverException

from bots.bot_configurations import load_conf
from bots.support_funcs import send_request_to_get_all_applicants_data_endpoint
from bots.vfs_appointment_checker_bot import VFSAppointmentCheckerBot


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

display = Display(visible=False, extra_args=[':25'], size=(2560, 1440)) 
display.start()


def upload_files(video_filename, recorder):
    recorder.terminate()
    sleep(7)
    recorder.wait(timeout=20)
    sleep(10)
    try:
            s3_file_object = s3_resource.Object(
                bucket_name=BUCKET_NAME, key='screenshot.png')
            s3_file_object.upload_file('/tmp/' + 'screenshot.png')
    except FileNotFoundError:
        print('Screenshot file not found')
    s3_file_object = s3_resource.Object(
        bucket_name=BUCKET_NAME, key=video_filename)
    s3_file_object.upload_file('/tmp/' + video_filename)


def rerun():
    print('Restarting')
    main()


def main():
    """
    This module will be used to start a bot which will be running
    without depending on Django instance.
    """
    # Check if we have applicants in our DB
    applicants_data = send_request_to_get_all_applicants_data_endpoint()
    if len(applicants_data) == 0:
        print('No applicants. Bot has stopped.')
        return
    
    video_filename = f'recording-{str(uuid4())}.mp4'
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
    except WebDriverException as wde:
        # When this exception occurs, usually Chrome is not available
        # so there's no point to record anything
        checker.driver.quit()
        print('Failed with WebDriverException: ', type(wde).__name__, ' ')
        print('Exception details:', wde)
        upload_files(video_filename, recorder)
        rerun()

    except Exception as e:
        checker.driver.quit()
        print('Failed with Exception: ', type(e).__name__, ' ')
        print('Exception details:', e)
        upload_files(video_filename, recorder)
        rerun()

    finally:
        # upload files for debugging
        upload_files(video_filename, recorder)

if __name__ == '__main__':
    main()