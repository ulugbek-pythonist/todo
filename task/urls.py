from django.urls import path

from task import views


urlpatterns = [
    path("", views.home, name="home"),
    # adding
    path("task/add/", views.add_task, name="add"),
    # retrieving
    path("done/<int:pk>/", views.make_done, name="done"),
    path("undone/<int:pk>/", views.make_undone, name="undone"),
    # updating
    path("edit/<int:pk>/", views.edit_task, name="edit"),
    # deleting
    path("delete/<int:pk>/", views.delete_task, name="delete"),
]
