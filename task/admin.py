from django.contrib import admin

from task.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("task", "is_done", "updated_at")
    search_fields = ("task",)
    list_editable = ("is_done",)


admin.site.register(Task, TaskAdmin)
