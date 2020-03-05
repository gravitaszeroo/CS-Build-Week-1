from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    return render(request, "hello_world.html")


def registration_page(request):
    return HttpResponse("<h1>This is the Registration Page!</h1>")


def login_page(request):
    return HttpResponse("<h1>This is the login page!</h1>")
