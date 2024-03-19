from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .forms import RegisterForm

from .models import Task


def home(request):
    tasks = Task.objects.all()
    return render(request, "home.html", {"tasks": tasks})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )

            user.set_password(password)
            user.save()

            return redirect('home')
    else:
        form = RegisterForm

        return render(request,"register.html",{"form":form})
