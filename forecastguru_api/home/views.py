# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@csrf_exempt
def login(request):
    if request.method == "POST":
        userID = json.loads(request.POST['userID'])
        try:
            user = User.objects.get(username=userID)
            auth = authenticate(username=userID, password=userID)
            if auth:
                login(request, user)
            return HttpResponse("registered")
        except Exception:
            user = User.objects.create(username=userID)
            user.set_password(userID)
            user.save()
            login(request, user)
            return HttpResponse("success")
    else:
        return render(request, "home/index.html", {})


@login_required
def home(request):
    return request.user.username