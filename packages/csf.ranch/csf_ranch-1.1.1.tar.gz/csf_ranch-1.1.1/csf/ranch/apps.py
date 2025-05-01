from django.apps import AppConfig


class RanchConfig(AppConfig):
    name = "csf.ranch"
    verbose_name = "Ranch"

    def ready(self):
        from . import signal_handlers  # noqa
