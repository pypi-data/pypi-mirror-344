import logging
import traceback as traceback_stdlib

from celery.signals import task_failure, task_unknown

from ..constants import TaskStatus
from ..controllers import persist_task
from ..lib.error_handling import log_errors

logger = logging.getLogger(__name__)


@task_failure.connect
@log_errors
def handle_task_failure(
    sender,
    task_id,
    exception,
    args,
    kwargs,
    traceback,
    einfo,
    **extra_kwargs,
):
    if sender.request.delivery_info:
        queue = sender.request.delivery_info.get("routing_key")
    else:
        queue = None
        logger.info(
            f"[Ranch task {task_id}] No delivery info found. Sender.request: {sender.request} # args: {args} # kwargs: {kwargs} # exception: {exception}",
        )

    try:
        persist_task(
            task_id,
            queue,
            sender.name,
            args,
            kwargs,
            traceback_stdlib.format_exc(),
            TaskStatus.FAILURE,
        )
    except Exception:
        # If anything goes wrong persisting the task to the DB,
        # we put it back in the Celery queue so that it is not
        # permanently lost. If that also fails, we should be
        # saved by acks_late=True.
        sender.retry(countdown=60)


@task_unknown.connect
@log_errors
def handle_task_unknown(sender, name, id, message, exc, **kwargs):
    try:
        queue = message.delivery_info.get("routing_key", "unknown")
    except Exception:
        queue = "unknown"

    persist_task(
        id,
        queue,
        name,
        message.payload[0],
        message.payload[1],
        traceback_stdlib.format_exc(),
        TaskStatus.UNKNOWN,
    )
