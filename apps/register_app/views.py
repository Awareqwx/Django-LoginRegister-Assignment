# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request, "registerApp/index.html")

def register(request):
    errors = User.objects.registerValidate(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect("/register/")
    else:
        try:
            User.objects.get(email=request.POST["email"])
        except:
            request.session["userid"] = User.objects.create(
                first_name = request.POST["firstname"],
                last_name = request.POST["lastname"],
                email = request.POST["email"],
                password_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            ).id
        else:
            messages.error(request, "Email already in use")
            return redirect("/register/")
        return redirect("/register/success/0")

def login(request):
    errors = User.objects.loginValidate(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect("/register/")
    else:
        try:
            User.objects.get(email=request.POST["email"])
        except:
            messages.error(request, "Invalid email or password!1")
            return redirect("/register/")
        else:
            if bcrypt.checkpw(request.POST["password"].encode(), User.objects.get(email=request.POST["email"]).password_hash.encode()):
                return redirect("/register/success/1")
            else:
                messages.error(request, "Invalid email or password!2")
                return redirect("/register/")
def success(request, loggedin):
    context = {}
    if loggedin == "0":
        context["loggedin"] = False
    else:
        context["loggedin"] = True
    context["name"] = User.objects.get(id=request.session["userid"]).first_name
    return render(request, "registerApp/success.html", context)