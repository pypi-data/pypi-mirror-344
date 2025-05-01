import logging

import rollbar
from celery.app import app_or_default, control
from datadog import initialize, statsd

from django.db.utils import Error

logger = logging.getLogger(__name__)
initialize()


def log_errors_and_send_to_rollbar(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Error:
            # If we receive any database-related exceptions, send SIGTERM--this may not be
            # necessary in every case, but it is safer
            logger.exception("Database error")
            rollbar.report_exc_info()
            statsd.increment("celery.signal-force-shutdown")
            controller = control.Control(app=app_or_default())
            controller.shutdown()
        except Exception:
            logger.exception("Ranch signal error")
            rollbar.report_exc_info()
            statsd.increment("celery.signal_error", value=1)
            raise

    return wrapper
