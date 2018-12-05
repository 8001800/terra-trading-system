from __future__ import absolute_import
from celery import Celery


application = Celery('proj', include=["proj.tasks", "proj.terrautil", "proj.terrachain"])
application.config_from_object("proj.settings")
 

if __name__ == '__main__':
    application.start()



