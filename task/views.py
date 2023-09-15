from django.shortcuts import get_object_or_404, redirect, render

from task.models import Task


# Create your views here.
def home(request):
    tasks = Task.objects.filter(is_done=False).order_by("-updated_at")

    completed_tasks = Task.objects.filter(is_done=True).order_by("-updated_at")

    context = {
        "tasks": tasks,
        "completed_tasks": completed_tasks,
    }
    return render(request, "home.html", context)


def add_task(request):
    task = request.POST["task"]
    Task.objects.create(task=task)
    return redirect("home")


def make_done(request, pk):
    selected_task = get_object_or_404(Task, pk=pk)
    selected_task.is_done = True
    selected_task.save()
    return redirect("home")


def make_undone(request, pk):
    selected_task = get_object_or_404(Task, pk=pk)
    selected_task.is_done = False
    selected_task.save()
    return redirect("home")


def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == "POST":
        task.task = request.POST["changed"]
        task.save()
        return redirect("home")
    else:
        context = {
            "selected": task,
        }

        return render(request, "edit.html", context)


def delete_task(request, pk):
    selected = get_object_or_404(Task, id=pk)
    selected.delete()
    return redirect("home")
