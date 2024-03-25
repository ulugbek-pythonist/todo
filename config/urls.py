from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('adminkapro/', admin.site.urls),
    path('volt/', include('admin_volt.urls')),
    path('', include('task.urls')),
    path("static/", serve,{'document_root': settings.MEDIA_ROOT}), 
    path("media/", serve,{'document_root': settings.STATIC_ROOT}), 
]

handler404 = "task.views.custom_page_not_found"