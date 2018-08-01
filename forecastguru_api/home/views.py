# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, HttpResponse


def login(request):
    if request.method == "POST":
        data = json.loads(request.POST['data'])
        return HttpResponse(json.dumps(data['authResponse']))
    else:
        return render(request, "home/index.html", {})

