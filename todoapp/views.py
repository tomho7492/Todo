from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import User
from .models import Todo
from django.contrib.auth import authenticate, login as auth_login, logout

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    toDos = Todo.objects.filter(User=request.user)
    context = {"toDos":toDos}
    for toDo in toDos:
        print(toDo.content)
    return render(request, 'homepage.html', context)

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == 'POST':
        email = request.POST["email-address"]
        password = request.POST["password"]
        print(email)
        print(password)
        user = User.objects.create_user(username=email, password=password)
        user.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, 'register.html')

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == 'POST':
        email = request.POST["email-address"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'login.html')
def addNote(request):
    if request.method == 'POST':
        content = request.POST["toDoContent"]
        toDo = Todo.objects.create(User=request.user, content=content)
        toDo.save()
        print(toDo)

    return HttpResponseRedirect(reverse("index"))

def remove(request):
    if request.method == 'POST':
        content = request.POST["deleteInput"]
        Todo.objects.filter(User=request.user, content=content).first().delete()

    return HttpResponseRedirect(reverse("index"))

def markCompleted(request):
    if request.method == 'POST':
        content = request.POST["completeInput"]
        print(f"content: {content}")

        todo = Todo.objects.filter(User=request.user, content=content).first()
        todo.completed = True
        print(f" marked complete: {todo.content} is {todo.completed}")
        todo.save()
    return HttpResponseRedirect(reverse("index"))

def edit(request):
    if request.method == 'POST':
        content = request.POST["editInput"]
        content = content.split(",")
        old = content[0]
        new = content[1]
        todo = Todo.objects.filter(User=request.user, content=old).first()
        todo.content = new
        todo.save()

    return HttpResponseRedirect(reverse("index"))