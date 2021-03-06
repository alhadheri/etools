import json
import os

from django.conf import settings

import requests
from tenant_schemas_celery.app import CeleryApp

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etools.config.settings.production')

app = CeleryApp('etools')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def send_to_slack(message):
    if settings.SLACK_URL:
        requests.post(
            settings.SLACK_URL,
            data=json.dumps({'text': message})
        )
