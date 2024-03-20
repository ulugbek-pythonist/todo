from django.urls import  path
from django.contrib.auth import views as auth_views

from .views import add_task, delete_task, edit_task, home, register

urlpatterns = [
    path("",home,name="home"),
    path("register/",register,name="register"), # type: ignore
    path("login/",auth_views.LoginView.as_view(template_name="login.html"),name="login"), # type: ignore
    path("logout/",auth_views.LogoutView.as_view(template_name="logout.html"),name="logout"), # type: ignore

    path("add_task/",add_task,name="add-task"), # type: ignore
    path("edit_task/<int:pk>/",edit_task,name="edit-task"), # type: ignore
    path("delete_task/<int:pk>/",delete_task,name="delete-task"), # type: ignore

]
