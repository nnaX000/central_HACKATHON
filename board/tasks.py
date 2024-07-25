from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from board.models import EveryList
from main.models import Notification

@shared_task
def check_due_tasks():
    now = timezone.now()
    due_time = now + timedelta(minutes=10)
    tasks = EveryList.objects.filter(due_date=due_time.date(), due_time__lte=due_time.time(), completed=False)
    
    for task in tasks:
        Notification.objects.create(
            user=task.user,
            message=f"할 일 '{task.task}'가 10분 후 시작됩니다."
        )