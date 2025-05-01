import logging

from celery.app import app_or_default, control
from datadog import initialize, statsd

from django.db.utils import Error

logger = logging.getLogger(__name__)
initialize()


def log_errors(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Error as err:
            # If we receive any database-related exceptions, send SIGTERM--this may not be
            # necessary in every case, but it is safer
            logger.exception("Database error", extra={"err": err})
            statsd.increment("celery.signal.error", tags = [f"exception:{type(err)}"])
            controller = control.Control(app=app_or_default())
            controller.shutdown()
        except Exception as err:
            logger.exception("Ranch signal error", extra={"err": err})
            statsd.increment("celery.signal.exception", tags = [f"exception:{type(err)}"])
            raise err

    return wrapper
