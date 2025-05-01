<p align="center">
  <img src="https://i.imgur.com/kshLe4w.png">
</p>

# Introduction

Simple and easy to use background tasks in Django without dependencies!

## ✨ Features

* ⚡ **Easy background task creation**
* 🛤️ **Multiple queue support**
* 🔄 **Automatic task retrying**
* 🛠️ **Well integrated with your chosen database**
* 🚫 **No additional dependencies**
* 🔀 **Supports both sync and async functions**


## Instalation

```bash
pip install django_firefly_tasks
```

## Setup
settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ###############
    'django_firefly_tasks',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },

    'loggers': {
        'django_firefly_tasks': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

## Quick Start
**views.py**
```python
from django.http.response import JsonResponse, Http404

from django_firefly_tasks.models import TaskModel
from django_firefly_tasks.decorators import task
from django_firefly_tasks.utils import task_as_dict


@task(queue="default", max_retries=0, retry_delay=0)
# param "queue" defines the queue in which the task will be placed
# param "max_retries" defines max retries on fail
# param "retry_delay" defines delay in seconds  between restarts
def add(i: int, j: int) -> int:
    return i + j


def task_view(request):
    """
    Example response
    ---
    {
        "id": 1,
        "func_name": "app.views.add",
        "status": "created",
        "not_before": null,
        "created": "2025-04-27T17:28:36.109Z",
        "retry_attempts": 0,
        "retry_delay": "0s",
        "max_retries": 0
    }
    """
    # pass function args to schedule method
    task = add.schedule(1, 3)
    return JsonResponse(task_as_dict(task))


def task_detail_view(request, task_id):
    """
    Example response
    ---
        4
    """
    try:
        task = TaskModel.objects.get(pk=task_id)
    except TaskModel.DoesNotExist:
        raise Http404("Task does not exist")
    # task.returned stores function returned data 
    return JsonResponse(task.returned, safe=False)
```
**urls.py**
```python
from django.urls import path

from .views import task_view, task_detail_view

urlpatterns = [
    path('task/', task_view, name='task_view'),
    path('task/<int:task_id>', task_detail_view, name='task_detail_view'),
]
```

Finally, run consumer. Default queue is called "default". **Consumer doesn't have  auto-reload, so when tasks changed it requires manual restart.**
```bash
./manage.py consume_tasks
```

## Contact
If you're missing something, feel free to add your own Issue or PR, which are, of course, welcome.
