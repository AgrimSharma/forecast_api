# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse


def login(request):
    if request.method == "POST":
        return HttpResponse(request.__dict__)
    else:
        return render(request, "home/index.html", {})

