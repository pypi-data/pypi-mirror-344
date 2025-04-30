from typing import Any

from django.core.management.base import BaseCommand

from ranch.controllers import rerun_logged_task
from ranch.models import LoggedTask

CHUNK_SIZE = 10000


class Command(BaseCommand):
    help = "Reruns all logged tasks."

    def handle(self, *args: Any, **options: Any) -> None:
        count = 0
        logged_tasks = LoggedTask.objects.all()[:CHUNK_SIZE]

        while logged_tasks.exists():
            for logged_task in logged_tasks:
                rerun_logged_task(logged_task)
                count += 1

                if count % 100 == 0:
                    print(f"Re-ran {count} tasks.")

            logged_tasks = LoggedTask.objects.all()[:CHUNK_SIZE]
