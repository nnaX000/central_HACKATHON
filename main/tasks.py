from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from board.models import EveryList
from .models import Notification

@shared_task
def send_task_reminders():
    now = timezone.now()
    reminder_time = now + timedelta(minutes=10)
    tasks = EveryList.objects.filter(due_date=reminder_time.date(), due_time__hour=reminder_time.hour, due_time__minute=reminder_time.minute)

    for task in tasks:
        Notification.objects.create(
            user=task.user,
            message=f'Reminder: Your task "{task.task}" is due in 10 minutes.'
        )
