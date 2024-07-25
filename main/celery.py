from celery import Celery
from celery.schedules import crontab

app = Celery('your_project_name')

app.conf.beat_schedule = {
    'check-due-tasks-every-minute': {
        'task': 'board.tasks.check_due_tasks',
        'schedule': crontab(minute='*/1'),  # 매 분마다 실행
    },
}

app.conf.timezone = 'UTC'
