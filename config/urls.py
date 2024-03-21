from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('adminkapro/', admin.site.urls),
    path('volt/', include('admin_volt.urls')),
    path('', include('task.urls')),
]

handler404 = "task.views.custom_page_not_found"