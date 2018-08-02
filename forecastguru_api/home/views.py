# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, random
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authentication.models import *
import re


def id_generator(fname, lname):
    r = re.compile(r"\s+", re.MULTILINE)
    return r.sub("", str(fname)).capitalize() + str(lname).capitalize() + str(random.randrange(1111, 9999))


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        userID = request.POST.get('userID')
        first_name = request.POST.get('first_name', "")
        last_name = request.POST.get('last_name', "")
        email = request.POST.get('email', "")
        try:
            user = User.objects.get(username=userID)
            auth = authenticate(request, username=userID, password=userID)

            if auth:
                login(request, auth)
            return HttpResponse("registered")
        except Exception:
            user = User.objects.create(username=userID, email=email,
                                       first_name=first_name,
                                       last_name=last_name)
            fuser = Authentication.objects.create(facebook_id=userID, first_name=first_name, last_name=last_name,
                                                  email=email)
            fuser.referral_code = id_generator(first_name, last_name)
            fuser.save()
            user.set_password(userID)
            user.save()
            auth = authenticate(request, username=userID, password=userID)
            if auth:
                login(request, auth)
            return HttpResponse("success")
    else:
        return render(request, "home/index.html", {"points": JoiningPoints.objects.latest('id').points})


def index(request):
    joining = JoiningPoints.objects.latest('id')
    return render(request, "home/main_page.html", {"points": joining.points})


@login_required
def referral_code(request):
    user = request.user.username
    auth = Authentication.objects.get(facebook_id=user)
    if auth.referral_status == 0:
        total = auth.joining_points + auth.points_won + auth.points_earned - auth.points_lost
        return render(request, "home/referral_code.html", {"first_name": auth.first_name,
                                                           "total": total})
    else:
        return redirect("/interest_select/")


@csrf_exempt
def check_referral(request):
    if request.method == "POST":
        code = request.POST.get('referral_code')
        user = request.user.username
        try:
            reff = Authentication.objects.get(referral_code=code)
            auth = Authentication.objects.get(facebook_id=user)
            auth.referral_status = 2
            auth.save()
            return HttpResponse("success")
        except Exception:
            return HttpResponse("error")

    else:
        user = request.user.username
        auth = Authentication.objects.get(facebook_id=user)
        auth.referral_status = 1
        auth.save()
        total = auth.joining_points + auth.points_won + auth.points_earned - auth.points_lost
        return redirect("/interest_select/")


@csrf_exempt
def interest(request):
    if request.method == 'GET':
        try:
            user = request.user.username
            profile = Authentication.objects.get(facebook_id=user)
            interest = UserInterest.objects.filter(user=profile)
            total = profile.joining_points + profile.points_won + profile.points_earned - profile.points_lost
            if len(interest) == 0:
                sub = Category.objects.all()
                return render(request, "home/interest_select.html", {"sub":sub,"heading": "Select Interest",
                                                                "title": "ForecastGuru",
                                                                "user": "Guest" if request.user.is_anonymous() else request.user.username,
                                                                "total": total
                                                                })
            else:
                return redirect("/live_forecast/")

        except Exception:
            return redirect("/login/")
    elif request.method == "POST":

        data = request.POST.getlist('data[]',"")
        if len(data) == 0:
            return HttpResponse("interest")
        elif len(data) > 0:
            interest = [int(d) for d in data]
            interest_list = SubCategory.objects.filter(id__in=interest)
            try:
                user = request.user.username
                profile = Authentication.objects.get(facebook_id=user)
                for i in interest_list:
                    interest = UserInterest.objects.filter(user=profile, interest=i)
                    if len(interest) == 0:
                        u = UserInterest.objects.create(user=profile, interest=i)
                        u.save()
                return HttpResponse("success")
            except Exception:
                return HttpResponse("login")


def live_forecast(request):
    return render(request, "home/live_forecast.html",{ "heading": "Live Forecast",
                                                                     "title": "ForecastGuru",
                                                                     "user": "Guest" if request.user.is_anonymous() else request.user.username
                                                                     })