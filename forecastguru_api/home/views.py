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
from random import randrange


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
        try:
            user = request.user.username
            auth = Authentication.objects.get(facebook_id=user)
            return render("/referral_code/")
        except Exception:
            return render(request, "home/index.html", {"points": JoiningPoints.objects.latest('id').points})


def index(request):
    try:
        user = request.user.username
        auth = Authentication.objects.get(facebook_id=user)
        return redirect("/live_forecast/")
    except Exception:
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


@login_required
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


@login_required
@csrf_exempt
def interest(request):
    if request.method == 'GET':
        try:
            user = request.user.username
            profile = Authentication.objects.get(facebook_id=user)
            interest = UserInterest.objects.filter(user=profile)
            total = profile.joining_points + profile.points_won + profile.points_earned - profile.points_lost
            if len(interest) == 0 and profile.interest_status == 0:
                sub = Category.objects.all().order_by('id')
                return render(request, "home/interest_select.html", {"sub":sub,"heading": "Select Interest",
                                                                "title": "ForecastGuru",
                                                                "first_name": request.user.first_name,
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


@login_required
def interest_skip(request):
    user = request.user.username
    auth = Authentication.objects.get(facebook_id=user)
    auth.interest_status = 1
    auth.save()
    return redirect("/live_forecast/")


@login_required
def live_forecast(request):
    return render(request, "home/live_forecast.html", {"heading": "Live Forecast",
                                                       "title": "ForecastGuru",
                                                       "first_name": "Guest" if request.user.is_anonymous()
                                                       else request.user.first_name
                                                       })


@csrf_exempt
def create_forecast(request):
    if request.method == 'POST':
        current = datetime.datetime.now()
        user = request.POST.get('user', '')
        category = request.POST.get('category', '')
        sub_category = request.POST.get('sub_cat', '')
        tags = request.POST.get('tags', '')
        heading = request.POST.get('heading', '')
        time = request.POST.get('time', '')
        date = request.POST.get('date', '')
        cat = Category.objects.get(id=category)
        sub_cat = SubCategory.objects.get(id=sub_category)
        expires = datetime.datetime.strptime(date + " " + time, "%d/%m/%Y %I:%M %p")

        if expires < current:
            return HttpResponse(json.dumps(dict(status=400, message='end')))
        try:
            users = Authentication.objects.get(user=request.user.username)
        except Exception:
            return HttpResponse(json.dumps(dict(status=400, message='Please Login')))
        private = Private.objects.get(id=2)
        verified = Verified.objects.get(id=2)
        approved = Approved.objects.get(id=2)
        status = Status.objects.get(name='In-Progress')
        ForeCast.objects.create(category=cat, sub_category=sub_cat,
                                user=users, heading=heading,
                                expire=expires,
                                start=datetime.datetime.now(),
                                approved=approved,
                                status=status, created=current,
                                private=private, verified=verified, tags=tags
                                )
        f = ForeCast.objects.get(category=cat, sub_category=sub_cat,
                                 user=users, heading=heading,
                                 )
        # fid = f.id
        f.user.forecast_created += 1
        f.user.save()
        f.save()
        yes = randrange(1000, 9000, 1000)
        no = randrange(1000, 9000, 1000)
        admin = Authentication.objects.get(facebook_id="admin")
        Betting.objects.create(forecast=f, users=admin, bet_for=yes, bet_against=no)
        # if private.name == 'no':
        #     try:
        #         NotificationPanel.objects.create(title="Forecast Guru", message="Thank You for creating a forecast " + str(heading),
        #                           url="https://forecast.guru/forecast/{}/".format(fid), user=users, status=0)
        #     except Exception:
        #         pass
        #     return HttpResponse(json.dumps(dict(status=200, message='Forecast Created', id=f.id)))
        # else:
        #
        #     InviteFriends.objects.create(user=admin, forecast=f)
        #     try:
        #         NotificationPanel.objects.create(title="Forecast Guru",
        #                                          message="Thank You for creating a forecast " + str(heading),
        #                                          url="https://forecast.guru/forecast/{}/".format(fid), user=users,
        #                                          status=0)
        #     except Exception:
        #         pass
        #     return HttpResponse(json.dumps(
        #         dict(status=200, message='Thank You for creating a private forecast', id=f.id)))

    else:
        # try:
        user = request.user.username
        profile = Authentication.objects.get(facebook_id=user)
        category = Category.objects.all().order_by('identifier')
        return render(request, 'home/create_forecast.html', {'category': category,
                                                        "current": datetime.datetime.now().strftime(
                                                            "%Y-%m-%d %H:%M"),
                                                        "user": "Guest" if request.user.is_anonymous() else request.user.first_name,
                                                        "heading": "Create Forecast",
                                                        "title": "ForecastGuru",
                                                        })
        # except Exception:
        #     return render(request, 'home/create_forecast_nl.html', {"heading": "Create Forecast",
        #                                                        "title": "ForecastGuru",
        #                                                        "user": "Guest" if request.user.is_anonymous() else request.user.first_name, })


@csrf_exempt
def get_sub_cat(request):
    if request.method == "POST":
        cat = Category.objects.get(id=int(request.POST.get('identifier', '')))
        sub = SubCategory.objects.filter(category=cat).order_by('identifier')
        data = [dict(id=x.id, name=x.name) for x in sub]
        return HttpResponse(json.dumps(dict(data=data, source=sub[0].source)))


@csrf_exempt
def get_sub_source(request):
    if request.method == "POST":
        cat = SubCategory.objects.get(id=int(request.POST.get('identifier', '')))
        return HttpResponse(json.dumps(cat.source))