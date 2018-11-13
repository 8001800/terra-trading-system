from celery.schedules import crontab


# Celery settings
BROKER_URL = 'redis://localhost:6379'
#CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
#CELERY_BEAT_SCHEDULE = {
#    'hello': {
#        'task': 'app.tasks.hello',
#        'schedule': crontab()  # execute every minute
#    }
#}
