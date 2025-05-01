from typing import Any

from django.core.management.base import BaseCommand

from ranch.models import LoggedTask


class Command(BaseCommand):
    help = "Deletd all failed tasks with the provided task name."

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--task_name", type=str, required=True)
        parser.add_argument(
            "--true-run",
            action="store_true",
            help="Actually delete the tasks.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        self.true_run = options.get("true_run") or False
        print("True run? ...", self.true_run)

        task_name = options.get("task_name")

        failed_tasks = LoggedTask.objects.filter(task_name=task_name, status="FAILURE")
        print(f"Found {failed_tasks.count()} failed tasks for '{task_name}'.")

        if not self.true_run:
            print("True run is False - skipping process.")
            return

        failed_tasks.delete()
