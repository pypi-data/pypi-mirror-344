import threading
import time
import uuid
from collections import Counter
from datetime import datetime

import billiard.compat
from celery.signals import (
    after_task_publish,
    before_task_publish,
    celeryd_after_setup,
    heartbeat_sent,
    task_failure,
    task_postrun,
    task_prerun,
    task_retry,
    task_success,
    task_unknown,
    worker_process_init,
)
from datadog import initialize, statsd
from dateutil import parser

from django.utils import timezone

from ..lib.error_handling import log_errors
from ..models import LoggedTask

initialize()
local = threading.local()

HEARTBEAT_METRICS_INTERVAL_SECONDS = 30


def _mem_rss_bytes():
    """
    `billiard.compat.mem_rss()` returns the memory in kB that the worker
    is using. Celery uses `mem_rss()` to enforce worker memory limits;
    Ranch uses the same function to track worker RSS over time and RSS
    change after each task is run. We convert to bytes (`* 1000`) to
    make the metrics easier to understand.
    """
    return billiard.compat.mem_rss() * 1000


@before_task_publish.connect
@log_errors
def add_metadata_to_task_headers(
    sender,
    body,
    exchange,
    routing_key,
    headers,
    properties,
    declare,
    retry_policy,
    **kwargs,
):
    eta = headers.get("eta")

    if isinstance(eta, str):
        eta = parser.parse(eta)

    queued_at = eta if eta else timezone.now()
    headers["__RANCH_QUEUED_AT"] = datetime.timestamp(queued_at)


@after_task_publish.connect
@log_errors
def send_metrics_on_publish(sender, headers, body, exchange, routing_key, **kwargs):
    statsd.increment(
        "celery.task.publish",
        value=1,
        tags=[f"task:{headers.get('task', 'unknown')}"],
    )


@task_prerun.connect
@log_errors
def store_metadata_before_task_runs(
    sender,
    task_id,
    task,
    args,
    kwargs,
    **extra_kwargs,
):
    local.task_received_at = time.time()
    try:
        local.task_queue = task.request.delivery_info.get("routing_key")
    except Exception:
        local.task_queue = None

    local.rss_before_bytes = _mem_rss_bytes()

    queued_at = getattr(task.request, "__RANCH_QUEUED_AT", None)
    if queued_at:
        wait_time_ms = (time.time() - queued_at) * 1000
        statsd.timing(
            "celery.task.wait_time",
            value=wait_time_ms,
            tags=[
                f"task:{task.name}",
                f"queue:{local.task_queue}",
            ],
        )


@task_postrun.connect
@log_errors
def send_metrics_after_task_runs(
    sender,
    task_id,
    task,
    args,
    kwargs,
    retval,
    state,
    **extra_kwargs,
):
    execution_time_ms = (time.time() - local.task_received_at) * 1000
    statsd.timing(
        "celery.task.execution_time",
        value=execution_time_ms,
        tags=[f"task:{task.name}", f"state:{state}", f"queue:{local.task_queue}"],
    )

    local.tasks_processed += 1
    statsd.gauge(
        "celery.worker.tasks_processed",
        value=local.tasks_processed,
        tags=[f"queue:{local.task_queue}", f"worker_id:{local.worker_id}"],
    )

    current_rss_bytes = _mem_rss_bytes()

    statsd.gauge(
        "celery.worker.rss_bytes",
        value=current_rss_bytes,
        tags=[f"queue:{local.task_queue}", f"worker_id:{local.worker_id}"],
    )

    rss_change_bytes = current_rss_bytes - local.rss_before_bytes
    statsd.increment(
        "celery.task.rss_change_bytes",
        value=rss_change_bytes,
        tags=[f"task{task.name}", f"queue:{local.task_queue}"],
    )


def _send_task_processed_metric(task_name, result):
    statsd.increment(
        "celery.task.processed",
        value=1,
        tags=[f"task:{task_name}", f"result:{result}", f"queue:{local.task_queue}"],
    )


@task_retry.connect
@log_errors
def send_metrics_on_task_retry(sender, request, reason, einfo, **kwargs):
    _send_task_processed_metric(sender.name, "retry")


@task_success.connect
@log_errors
def send_metrics_on_task_success(sender, result, *args, **kwargs):
    _send_task_processed_metric(sender.name, "success")


@task_failure.connect
@log_errors
def send_metrics_on_task_failure(
    sender,
    task_id,
    exception,
    args,
    kwargs,
    traceback,
    einfo,
    **extra_kwargs,
):
    _send_task_processed_metric(sender.name, "failure")


@task_unknown.connect
@log_errors
def send_metrics_on_task_unknown(sender, name, id, message, exc, **kwargs):
    statsd.increment("celery.task.unknown", value=1, tags=[f"task:{name}"])


@celeryd_after_setup.connect
@log_errors
def store_metadata_on_worker_parent_start(sender, instance, conf, **kwargs):
    local.worker_instance = instance
    local.app_config = conf

    # worker_queues is a dict of queue name to Celery queue instance, for
    # all queues this worker is configured to process
    # Don't freak out about the variable named amqp, yes it is
    # called this even if you're using Redis. Celery is jank.
    local.worker_queues = instance.app.amqp.queues

    # broker_type is a string, "amqp" or "redis" (or others but these
    # are the ones we expect to use)
    local.broker_type = instance.app.broker_connection().transport_cls

    local.last_send_on_heartbeat = 0


@worker_process_init.connect
@log_errors
def store_metadata_on_worker_child_start(sender, **kwargs):
    # number of tasks processed over the lifetime of each worker *child* process
    local.tasks_processed = 0
    local.worker_id = str(uuid.uuid4())


def _error_queue_tags(task):
    return [f"queue:{task.queue}", f"task:{task.task_name}"]


def _send_error_queue_metrics():
    tasks = LoggedTask.objects.all()

    if tasks:
        counts = Counter(tuple(_error_queue_tags(task)) for task in tasks)

        for tags, count in counts.items():
            statsd.gauge("celery.queue.errors.length", value=count, tags=list(tags))

    else:
        statsd.gauge("celery.queue.errors.length", value=0)


@heartbeat_sent.connect
@log_errors
def send_queue_metrics_on_heartbeat(sender, **kwargs):
    if time.time() - HEARTBEAT_METRICS_INTERVAL_SECONDS < local.last_send_on_heartbeat:
        return

    _send_error_queue_metrics()

    local.last_send_on_heartbeat = time.time()
