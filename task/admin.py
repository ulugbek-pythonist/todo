from django.contrib import admin
from .models import Task,Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["task","category","doer","is_done"]