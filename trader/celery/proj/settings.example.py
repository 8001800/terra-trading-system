from celery.schedules import crontab
from datetime import timedelta

# Celery settings
BROKER_URL = 'redis://localhost:6379'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379'

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "",
    "port": 27017,
    "database": "",
    "user": "",
    "password": "",
    "taskmeta_collection": "",
}



CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'




CELERYBEAT_SCHEDULE = {
    'add': {
        'task': 'proj.test.add',
        'schedule': timedelta(seconds=10),
        'args': (16, 16)
    }
}