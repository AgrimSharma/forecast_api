# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.method == "POST":
        # data = json.loads(request.POST['perms'])
        # return HttpResponse(json.dumps(data['authResponse']))
        return HttpResponse(json.dumps(request.__dict__))
    else:
        return render(request, "home/index.html", {})

