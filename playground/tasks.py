from time import sleep
from celery import shared_task


@shared_task
def notify_customers(message):
    print("Sending 20k emails...")
    print(message)
    sleep(20)
    print("Emails were successfully send!")
