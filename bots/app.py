import time


def lambda_handler(event, context):
    print('hello world', event)
    time.sleep(10)
    print('woke up after 10 secs', event)
    return True
