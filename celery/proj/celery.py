from __future__ import absolute_import
import os
from celery import Celery


app = Celery('proj',include=["proj.tasks"])

app.config_from_object("proj.settings")
 

if __name__ == "__main__":
	app.start()     



