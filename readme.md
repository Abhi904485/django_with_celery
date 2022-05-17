## Installing Rabbitmq in mac

* brew install rabbitmq
* brew services start rabbitmq

## Installing redis in mac

* brew install redis
* brew services start redis

## python Modules should be installed

- celery
- celery-progress
- redis
- flower
- django

## Necessary Rabbitmq Configurations

* rabbitmq-plugins enable rabbitmq_management

* rabbitmqctl add_user root root

* rabbitmqctl set_user_tags root administrator

* rabbitmqctl add_vhost sample_host

* rabbitmqctl set_permissions -p sample_host root ".*" ".*" ".*"

* Rabbitmq management page access url : http://localhost:15672/#/users/root

## how to run celery

`start one Worker node`

- pip install celery and pip install redis is required

* celery -A django_with_celery worker -l info

`start flower feom celery for watching and monitoring if redis is broker`

- pip install flower is mandatory

* celery -A django_with_celery --broker=redis://localhost:6379/0 flower --address=127.0.0.1 --port=5555

`start flower feom celery for watching and monitoring if rabbitmq is broker`

* celery -A django_with_celery --broker=pyamqp://root:root@localhost:5672/sample_host flower --address=127.0.0.1
  --port=5555

`start beat from celery for chrontab or scheduled task`

- For that we need to add in settings.py file

```
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# When we want to store task result into DB then comment above line and uncomment below line
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_CACHE_BACKEND = "django-cache"

CELERY_BEAT_SCHEDULE = {
    "default_schedule": {
        'task': 'progressbar.task.send_mail',
        'schedule': 5,
        'args': ("khusbu@gmail.com",)
    },
    # Executes every wednesday at 2:34am
    'cron_schedule': {
        'task': 'progressbar.task.send_mail',
        'schedule': crontab(hour=2, minute=34, day_of_week=3),
        'args': ('Abhishek@gmail.com',)
    },
    # For Solar pip install ephem is required 
    'solar_schedule': {
        'task': 'my_app.tasks.send_notification',
        'schedule': solar('sunset', -37.81753, 144.96715),
    },
}
```

* celery -A django_with_celery beat -l info

`start celery beat with custom schedulers`

- required python module django-celery-beat
- add into installed apps
- migrate

* celery -A django_with_celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

`Save Task Result under Table`

- required python module django-celery-result
- add into installed apps
- migrate
- CELERY_RESULT_BACKEND = 'django-db' and CELERY_CACHE_BACKEND = "django-cache" 