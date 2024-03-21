🔵 To Do

Bu loyiha ham django freymvorki yordamida qilingan. Quyida unda bor xususiyat(feature)larni aytib o'taman.

Foydalanuvchilarga oid:

🟢 Ro'yhatdan o'tish

🟢 Tizimga kirish/chiqish


Topshiriqlar(tasks)ga oid:

🔴 Task qo'shish (kategoriyasi bilan)

🔴 Taskni tahrirlash (kategoriyasi bilan)

🔴 Taskni o'chirish

🔴 Ma'lum kategoriyaga oid tasklarni ko'rish

🔴 Taskni bajarilgan yoki bajarilmagan qilib belgilash


Qo'shimcha xususiyatlar:

✅ Boshqa foydalanuvchilarning tasklarini ko'rolmaslik va ularni o'zgartira olmaslik

✅ Custom 404 sahifa

✅ Admin panel orqali qaysi turdagi tasklar ko'p bajarilayotganini foizlarda kuzatish

Endi o'rganuvchilar uchun ayrim kodlarni quyida keltiraman:<br/>

# Eng avval `task.models.py` faylga nazar tashlaymiz:
<br/>

```
from django.db import models
from django.contrib.auth.models import User
from config.models import BaseModel



class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Task(BaseModel):
    task = models.CharField(max_length=300)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="categories")
    doer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="users")
    is_done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.task[:10] + "..."
    

```

Ha aytganday BaseModel quyidagicha:

```
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

# Barcha tasklar:

```
from django.shortcuts import get_object_or_404, redirect, render

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
```


# Task qo'shish uchun yozilgan view: 
<br/>

```
from django.contrib.auth.decorators import login_required

@login_required
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
```

# Taskni tahrirlash uchun yozilgan view:

```
@login_required
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
```

# Taskni o'chirish uchun:

```
@login_required
def delete_task(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    task.delete()
    return redirect("home")
```

# Taskni bajarilgan yoki bajarilmagan deb belgilash:

```
# bajarilmagan deb belgilash
@login_required
def mark_as_undone(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    task.is_done = False
    task.save()

    return redirect("home")

# bajarilgan deb belgilash
@login_required
def mark_as_done(request, pk):
    task = Task.objects.filter(id=pk, doer=request.user).first()

    if task is None:
        return render(request, "error.html", {"user": request.user})

    task.is_done = True
    task.save()

    return redirect("home")
```

# Kategoriyasi bo'yicha tasklarni ko'rish:

```
@login_required
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
```

# Admin panel uchun kichik statistik ma'lumot:
`admin.py` faylda quyidagilar

```
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
```

# Ro'yhatdan o'tish:
`views.py` da

```
from django.contrib.auth.models import User
from .forms import RegisterForm


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
```

`forms.py` da

```
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password"]

```


# Login va logout uchun default view lardan foydalanilgan, faqat templatelar yozib qo'yilgan xolos:

`urls.py` da

```
from django.urls import  path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/",auth_views.LoginView.as_view(template_name="login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(template_name="logout.html"),name="logout"), 
]
```

`settings.py` da

```
LOGIN_REDIRECT_URL = 'home'
```