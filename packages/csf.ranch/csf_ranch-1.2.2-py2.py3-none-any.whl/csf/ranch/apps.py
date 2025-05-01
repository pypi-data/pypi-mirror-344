from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class RanchConfig(AppConfig):
    name = "csf.ranch"
    verbose_name = "Ranch"

    def ready(self):
        env = settings.RANCH.get("env")
        service = settings.RANCH.get("service")

        if not all([env, service]):
            raise ImproperlyConfigured(
                "csf.ranch must be configured with env and service parameters."
            )

        # self.module._collector = metrics.Collector(
        #     namespace="csf.ranch",
        #     tags={"env": env, "service": service, "csf-service-name": service},
        # )

        from . import signal_handlers  # noqa