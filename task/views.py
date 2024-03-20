from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

from .models import Category, Task


@login_required # type: ignore
def add_task(request):
    if request.method == "POST":
        try:
            task = request.POST["task"]
            category = request.POST["category"]
            category = get_object_or_404(Category,name=category)
            print(task,category)
        except Exception:
            return redirect("home")

        if task is not None:
            Task.objects.create(task=task,category=category,doer=request.user)

        return redirect("home")


def home(request):
    categories = Category.objects.all()
    try:
        tasks = Task.objects.filter(doer=request.user)
    except Exception:
        tasks = []

    return render(
        request,
        "home.html",
        {
            "tasks": tasks,
            "categories": categories,
        },
    )


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

            return redirect("login")
        else:
            form = RegisterForm
            return render(request, "register.html", {"form": form})
    else:
        form = RegisterForm

        return render(request, "register.html", {"form": form})
