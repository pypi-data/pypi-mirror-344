from importlib import import_module

# Use kombu's JSON loading/dumping - they extend native json loads/dumps to handle some
# non-natively supported types (ex. datetimes).
from kombu.utils import json

from .exceptions import TaskNotFoundError
from .models import LoggedTask


def persist_task(
    task_id,
    queue,
    task_name,
    args,
    kwargs,
    stacktrace,
    status,
):
    return LoggedTask.objects.create(
        id=task_id,
        queue=queue,
        task_name=task_name,
        args=json.dumps(args),
        kwargs=json.dumps(kwargs),
        stacktrace=stacktrace,
        status=status,
    )


def rerun_logged_task(logged_task):
    task_name = logged_task.task_name.split(".")[-1]
    module_path = logged_task.task_name.replace(f".{task_name}", "")

    module = import_module(module_path)
    task_func = getattr(module, task_name, None)

    if task_func is None:
        raise TaskNotFoundError()

    args = json.loads(logged_task.args)
    kwargs = json.loads(logged_task.kwargs)
    task_func.delay(*args, **kwargs)
    logged_task.delete()
