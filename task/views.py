from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

from .models import Category, Task

def custom_page_not_found(request,exception):
    return render(request,"404.html",status=404)


@login_required  # type: ignore
def filtered_tasks(request, slug):
    category = get_object_or_404(Category, slug=slug)
    tasks = Task.objects.filter(category=category, doer=request.user)

    if tasks.count() <= 0:
        return render(request, "error.html", {"user": request.user})

    return render(
        request,
        "tasks.html",
        {
            "tasks": tasks,
            "category": category,
        },
    )


@login_required  # type: ignore
def mark_as_undone(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    task.is_done = False
    task.save()

    return redirect("home")


@login_required  # type: ignore
def mark_as_done(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    task.is_done = True
    task.save()

    return redirect("home")


@login_required  # type: ignore
def delete_task(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    task.delete()
    return redirect("home")


@login_required  # type: ignore
def edit_task(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()
    categories = Category.objects.all()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    if request.method == "POST":
        try:
            changed = request.POST["changed"]
            category = request.POST["category"]
            category = get_object_or_404(Category, name=category)
        except Exception:
            return redirect("home")

        task.task = changed if len(changed) > 0 else task.task
        task.category = category
        task.save()

        return redirect("home")
    else:
        return render(
            request,
            "edit.html",
            {
                "task": task,
                "categories": categories,
            },
        )


@login_required  # type: ignore
def add_task(request):
    if request.method == "POST":
        try:
            task = request.POST["task"]
            category = request.POST["category"]
            category = get_object_or_404(Category, name=category)
            print(task, category)
        except Exception:
            return redirect("home")

        if task is not None:
            Task.objects.create(task=task, category=category, doer=request.user)

        return redirect("home")


def home(request):
    categories = Category.objects.all()
    try:
        tasks = Task.objects.filter(doer=request.user, is_done=False)
        done_tasks = Task.objects.filter(doer=request.user, is_done=True)
    except Exception:
        tasks = []
        done_tasks = []

    return render(
        request,
        "home.html",
        {"tasks": tasks, "categories": categories, "completed_tasks": done_tasks},
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
