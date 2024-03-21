from django.contrib import admin
from .models import Task,Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}
    list_display = ['name','get_category_percentage']
    
    def get_category_percentage(self, obj):
        total_tasks = Task.objects.count()
        category_tasks = Task.objects.filter(category=obj).count()
        if total_tasks == 0:
            return 0
        return round((category_tasks / total_tasks) * 100, 2)

    get_category_percentage.short_description = 'Category Percentage'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["task","category","doer","is_done"]
