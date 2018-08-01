# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@csrf_exempt
def login(request):
    if request.method == "POST":
        userID = json.loads(request.POST['userID'])
        try:
            user = User.objects.get(username=userID)
            return HttpResponse("User Already Exists")
        except Exception:
            user = User.objects.create(username=userID)
            user.save()
            return HttpResponse("User Registered")
    else:
        return render(request, "home/index.html", {})

