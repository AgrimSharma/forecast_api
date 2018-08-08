# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Sum
import json, random
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authentication.models import *
import re
from random import randrange
import datetime

current = datetime.datetime.now()


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
            user = User.objects.create(username=userID,
                                       email=email,
                                       first_name=first_name,
                                       last_name=last_name
                                       )
            fuser = Authentication.objects.create(facebook_id=userID,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  email=email
                                                  )
            fuser.referral_code = id_generator(first_name, last_name)
            fuser.points_earned = JoiningPoints.objects.latest('id').points
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
            return redirect("/referral_code/")
        except Exception:
            return render(request, "home/index.html", {
                "points": JoiningPoints.objects.latest('id').points
            })


def index(request):
    try:
        user = request.user.username
        auth = Authentication.objects.get(facebook_id=user)
        return redirect("/live_forecast/")
    except Exception:
        joining = JoiningPoints.objects.latest('id')
        return render(request, "home/main_page.html", {
            "points": joining.points
        })


@login_required
def referral_code(request):
    user = request.user.username
    auth = Authentication.objects.get(facebook_id=user)
    if auth.referral_status == 0:
        total = auth.joining_points + auth.points_won_public + auth.points_won_private + auth.points_earned \
                - auth.points_lost_public - auth.points_lost_private
        return render(request, "home/referral_code.html", {
            "first_name": auth.first_name,
            "total": total
        })
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
        total = auth.joining_points + auth.points_won_public + auth.points_won_public + auth.points_earned - auth.points_lost
        return redirect("/interest_select/")


@login_required
@csrf_exempt
def interest(request):
    if request.method == 'GET':
        try:
            user = request.user.username
            profile = Authentication.objects.get(facebook_id=user)
            interest = UserInterest.objects.filter(user=profile)
            total = profile.joining_points + profile.points_won_public\
                    + profile.points_won_private + profile.points_earned - profile.points_lost_public - profile.points_lost_private
            if len(interest) == 0 and profile.interest_status == 0:
                sub = Category.objects.all().order_by('id')
                return render(request, "home/interest_select.html", {
                    "sub": sub,
                    "heading": "Select Interest",
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


def live_forecast(request):
    data = []
    try:
        user = request.user.username
        profile = Authentication.objects.get(facebook_id=user)
        interest = UserInterest.objects.filter(user=profile)
        intrest = [i.interest.id for i in interest]
        forecast_live = ForeCast.objects.filter(status__name='Progress',
                                                sub_category__id__in=intrest).order_by("expire")
    except Exception:
        forecast_live = ForeCast.objects.filter(status__name='Progress').order_by("expire")
    print(forecast_live)

    for f in forecast_live:
        date = current.date()

        bet_start = f.expire.date()
        if date == bet_start:
            start = f.expire + datetime.timedelta(hours=5, minutes=30)
            start = start.time()
            today = 'yes'
        else:
            start = f.expire

            today = "no"
        betting_for = Betting.objects.filter(forecast=f, bet_for__gt=0).count()
        betting_against = Betting.objects.filter(forecast=f, bet_against__gt=0).count()
        try:
            total_wagered = betting_against + betting_for
            bet_for = Betting.objects.filter(forecast=f).aggregate(bet_for=Sum('bet_for'))['bet_for']
            bet_for_user = Betting.objects.filter(forecast=f, users=profile).aggregate(bet_for=Sum('bet_for'))[
                'bet_for']
            bet_against = Betting.objects.filter(forecast=f).aggregate(bet_against=Sum('bet_against'))[
                'bet_against']
            bet_against_user = \
                Betting.objects.filter(forecast=f, users=profile).aggregate(bet_against=Sum('bet_against'))[
                    'bet_against']
            totl = bet_against + bet_for
            percent_for = (bet_for / totl) * 100
            percent_against = (100 - percent_for)

            total = Betting.objects.filter(forecast=f).count()
        except Exception:
            total_wagered = 0
            bet_against_user = 0
            bet_for_user = 0
            percent_for = 0
            percent_against = 0
            bet_for = 0
            bet_against = 0
            total = Betting.objects.filter(forecast=f).count()
        data.append(dict(percent_for=int(percent_for), percent_against=int(percent_against), forecast=f,
                         total=total, start=start, total_user=betting_for + betting_against,
                         betting_for=betting_for, betting_against=betting_against, today=today,
                         participants=total_wagered, bet_for=bet_for,
                         bet_against=bet_against,
                         bet_for_user=bet_for_user if bet_for_user else 0,
                         bet_against_user=bet_against_user if bet_against_user else 0))
    print(data)
    return render(request, 'home/live_forecast.html', {"live": data,
                                                  "heading": "Forecasts",
                                                  "title": "ForecastGuru",
                                                  "first_name": "Guest" if request.user.is_anonymous() else request.user.first_name})


@csrf_exempt
def bet_post(request):
    if request.method == 'POST':
        try:
            user = request.user.username
            account = Authentication.objects.get(facebook_id=user)
        except Exception:
            return HttpResponse(json.dumps(dict(message='login')))
        vote = request.POST.get('vote')
        points = int(request.POST.get('points'))
        if int(points) % 1000 != 0:
            return HttpResponse(json.dumps(dict(message='Points should be multiple of 1000')))
        forecast = request.POST.get('forecast')
        forecasts = ForeCast.objects.get(id=forecast)
        if account.points_earned - points > 0 or account.points_won_public - points > 0 or account.points_won_private- points > 0:
            try:
                b = Betting.objects.get(forecast=forecasts, users=account)
                if vote == 'email':
                    b.bet_for += points
                    if b.users.points_earned >= points:
                        b.users.points_earned -= points
                    elif b.users.points_won_public >= points:
                        b.users.points_won_public -= points
                    else:
                        b.users.points_won_private -= points
                    b.users.save()
                    b.save()
                else:
                    b.bet_against += points
                    if b.users.points_earned >= points:
                        b.users.points_earned -= points
                    elif b.users.points_won_public >= points:
                        b.users.points_won_public -= points
                    else:
                        b.users.points_won_private -= points
                    b.users.save()
                    b.save()
            except Exception:
                if vote == 'email':
                    b = Betting.objects.create(forecast=forecasts, users=account, bet_for=points, bet_against=0)
                    if b.users.points_earned >= points:
                        b.users.points_earned -= points
                    elif b.users.points_won_public >= points:
                        b.users.points_won_public -= points
                    else:
                        b.users.points_won_private -= points
                    b.users.forecast_participated += 1
                    b.users.save()
                    b.save()
                else:
                    b = Betting.objects.create(forecast=forecasts, users=account, bet_for=0, bet_against=points)
                    if b.users.points_earned >= points:
                        b.users.points_earned -= points
                    elif b.users.points_won_public >= points:
                        b.users.points_won_public -= points
                    else:
                        b.users.points_won_private -= points
                    b.users.forecast_participated += 1
                    b.users.save()
                    b.save()
            return HttpResponse(json.dumps(dict(message='success')))
        else:
            return HttpResponse(json.dumps(dict(message='balance')))
    else:
        return HttpResponse(json.dumps(dict(message='Please use POST')))


@csrf_exempt
def get_forecast(request):
    if request.method == "POST":
        # try:
        user = request.user.username
        profile = Authentication.objects.get(facebook_id=user)
        forecast = ForeCast.objects.get(id=request.POST.get('id', ''))
        return HttpResponse(json.dumps(dict(heading=forecast.heading, id=forecast.id)))
    else:

        return HttpResponse(json.dumps(dict(error="Try again later")))


@csrf_exempt
def create_forecast(request):
    if request.method == 'POST':
        current = datetime.datetime.now()
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
            users = Authentication.objects.get(facebook_id=request.user.username)
        except Exception:
            return HttpResponse(json.dumps(dict(status=400, message='Please Login')))
        private = Private.objects.get(id=1)
        status = Status.objects.get(name='Progress')
        ForeCast.objects.create(category=cat, sub_category=sub_cat,
                                user=users, heading=heading,
                                expire=expires,
                                status=status, created=current,
                                private=private, tags=tags
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
        bet = Betting.objects.create(forecast=f, users=admin, bet_for=yes, bet_against=no)
        bet.save()
        return HttpResponse(json.dumps(
            dict(status=200, message='Thank You for creating a private forecast', id=f.id)))

    else:
        try:
            user = request.user.username
            profile = Authentication.objects.get(facebook_id=user)
            category = Category.objects.all().order_by('identifier')
            return render(request, 'home/create_forecast.html', {
                'category': category,
                "current": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "user": "Guest" if request.user.is_anonymous() else request.user.first_name,
                "heading": "Create Forecast",
                "title": "ForecastGuru",
            })
        except Exception:
            return render(request, 'home/create_forecast_nl.html', {
                "heading": "Create Forecast",
                "title": "ForecastGuru",
                "user": "Guest" if request.user.is_anonymous() else request.user.first_name, })


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


def betting(request, userid):
    forecast = ForeCast.objects.get(id=userid)
    approved = "Yes" if forecast.private.name == 'Yes' and forecast.status.name == 'Progress' else 'No'
    if forecast.status.name == 'Progress':
        status = 'Currently Live'
    elif forecast.status.name == 'Closed':
        status = 'Currently Closed'
    else:
        status = 'Result Declared'
    try:
        if forecast.won.name.lower() == 'yes':
            won = 'yes'
        elif forecast.won.name.lower() == 'no':
            won = 'no'
    except Exception:
        won = "NA"
    expires = forecast.expire + datetime.timedelta(hours=5, minutes=30)
    end_date = datetime.datetime.strftime(expires, '%b %d, %Y')
    end_time = datetime.datetime.strftime(expires, '%H:%M')
    # try:/
    if request.user.is_anonymous():
        users = "Guest"
    else:
        users = request.user.username
    if forecast.private.name == 'N':
        betting_for = Betting.objects.filter(forecast=forecast, bet_for__gt=0).count()
        betting_against = Betting.objects.filter(forecast=forecast, bet_against__gt=0).count()

        betting_sum = Betting.objects.filter(forecast=forecast).aggregate(
            bet_for=Sum('bet_for'), bet_against=Sum('bet_against'))
        try:
            total_wagered = betting_sum['bet_for'] + betting_sum['bet_against']
        except Exception:
            total_wagered = 0

        try:
            percent = round((betting_for / (betting_for + betting_against)) * 100, 2)
        except Exception:
            percent = 0
        try:
            success = Authentication.objects.get(facebook_id=request.user.username)
            success = success.successful_forecast
        except Exception:
            success = 0
        try:
            sums = betting_sum['bet_for'] + betting_sum['bet_against']
        except Exception:
            sums = 0

        try:
            social = Authentication.objects.get(facebook_id=request.user.username)
            bet_for_user = Betting.objects.get(forecast=forecast, users=social).bet_for
            bet_against_user = Betting.objects.get(forecast=forecast, users=social).bet_against
            market_fee = sums * 0.10 if forecast.user == social else 0
        except Exception:
            bet_against_user = 0
            bet_for_user = 0
            market_fee = 0
        if forecast.won and sums > 0:
            if forecast.won.lower() == "yes":
                ratio = round(betting_sum['bet_for'] / sums, 2) + 1
                earned = bet_for_user * ratio
                market_fee_paid = earned * 0.10
                total_earning = earned - market_fee_paid + market_fee
            elif forecast.won.lower() == "no":
                ratio = round(betting_sum['bet_against'] / sums, 2) + 1
                earned = bet_against_user * ratio
                market_fee_paid = earned * 0.10
                total_earning = earned - market_fee_paid + market_fee
        else:
            ratio = "NA"
            earned = 0
            market_fee_paid = earned * 0.10
            total_earning = earned - market_fee_paid + market_fee

        return render(request, 'home/betting.html', {'forecast': forecast, 'betting': betting,
                                                'bet_for': betting_sum['bet_for'] if betting_sum['bet_for'] else 0,
                                                'against': betting_sum['bet_against'] if betting_sum[
                                                    'bet_against'] else 0,
                                                'total': total_wagered if total_wagered else 0,
                                                "end_date": end_date, "end_time": end_time,
                                                'status': status, "percent": percent,
                                                "success": success,
                                                "users": request.user.first_name,
                                                "sums": sums,"earned": int(earned),
                                                "approved": approved,"ratio": ratio,
                                                "user": users,"won": won,"market_fee_paid": int(market_fee_paid),
                                                "heading": "Forecast Details",
                                                "title": "ForecastGuru","private": "no",
                                                "bet_against_user":bet_against_user,
                                                "bet_for_user" : bet_for_user, "market_fee": int(market_fee),
                                                "total_earn": int(total_earning)
                                                })
    elif forecast.private.name == 'Yes':
        points = []
        betting_sum = Betting.objects.filter(forecast=forecast).aggregate(
            bet_for=Sum('bet_for'), bet_against=Sum('bet_against'))
        sums = betting_sum['bet_for'] + betting_sum['bet_against']
        if forecast.won.name.lower() == "yes":
            ratio = round(betting_sum['bet_for'] / sums, 2) + 1
            won = "yes"
        elif forecast.won.name.lower() == "no":
            ratio = round(betting_sum['bet_against'] / sums, 2) + 1
            won = "no"
        else:
            ratio = "NA"
            won = "NA"
        return render(request, 'home/betting.html', {'forecast': forecast, 'betting': betting,
                                                    "approved": approved,
                                                    "user": users,'status': status,
                                                    "users": forecast.user.first_name,
                                                    "end_date": end_date, "end_time": end_time,
                                                    "won": won,"ratio": ratio,
                                                    "heading": "Forecast Details",
                                                    "title": "ForecastGuru", "private": "yes",
                                                    "points": points})


@csrf_exempt
def result_save(request):
    if request.method == "POST":
        user = request.user
        profile = Authentication.objects.get(facebook_id=user.username)
        vote = request.POST.get("vote","")
        id = request.POST.get('forecast', '')
        if vote == 'email':
            vote = 'yes'
        else:
            vote = 'no'

        verified = Verified.objects.get(id=1)
        status = Status.objects.get(name='Closed')
        forecast = ForeCast.objects.get(id=int(id))
        ForeCast.objects.filter(id=id).update(won=vote, status=status, verified=verified)
        return HttpResponse(request.path)
    else:
        return HttpResponse(json.dumps(dict(error="Try again later")))