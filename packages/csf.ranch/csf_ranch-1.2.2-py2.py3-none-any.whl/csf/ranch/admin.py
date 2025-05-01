import json

from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from django.utils.html import format_html

from .controllers import rerun_logged_task
from .models import LoggedTask


class LoggedTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "queue",
        "task_name",
        "created_at",
        "args",
        "kwargs",
        "status",
    )
    list_filter = ("task_name", "queue", "status")

    fields = readonly_fields = (
        "id",
        "queue",
        "created_at",
        "task_name",
        "admin_args",
        "admin_kwargs",
        "admin_stacktrace",
        "status",
    )
    ordering = ("-created_at",)

    actions = ["retry_logged_tasks", "delete_selected"]

    def retry_logged_tasks(self, request, queryset):
        opts = self.model._meta

        if request.POST.get("post") == "yes":
            for logged_task in queryset:
                rerun_logged_task(logged_task)
            count = queryset.count()
            message = f"Retried {count} Logged Task items"
            self.message_user(request, message, messages.SUCCESS)
            # Return None to display the change list page again.
            return None

        context = {
            "title": "Retry Tasks?",
            "queryset": queryset,
            "opts": opts,
            "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
            "media": self.media,
        }

        return TemplateResponse(
            request,
            "admin/retry_task_confirmation.html",
            context=context,
        )

    retry_logged_tasks.short_description = "Retry Selected Tasks"

    def admin_stacktrace(self, logged_task):
        return format_html("<br/><pre>{}</pre>", logged_task.stacktrace)

    def admin_args(self, logged_task):
        args = json.loads(logged_task.args)
        return format_html("<br/><pre>{}</pre>", json.dumps(args, indent=4))

    def admin_kwargs(self, logged_task):
        kwargs = json.loads(logged_task.kwargs)
        return format_html("<br/><pre>{}</pre>", json.dumps(kwargs, indent=4))


admin.site.register(LoggedTask, LoggedTaskAdmin)
