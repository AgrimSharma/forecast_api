from rest_framework import serializers
from .models import *
import string, random
import re


def id_generator(name):
    r = re.compile(r"\s+", re.MULTILINE)
    return r.sub("", str(name)).capitalize() + str(random.randrange(1111, 9999))


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Authentication
        fields = ["id", "facebook_id", "full_name", 'gender', "email", "mobile"]

    def create(self, validated_data):
        auth = Authentication.objects.create(**validated_data)
        joining = JoiningPoints.objects.get(id=1).points
        auth.joining_points = joining
        auth.referral_code = id_generator(auth.full_name)
        return auth


class LastLoginSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    login_date = serializers.DateField()

    class Meta:
        model = Authentication
        fields = ["user_id", "login_date"]


class ForecastSerializers(serializers.ModelSerializer):
    class Meta:
        model = ForeCast
        fields = ["id", "category", "sub_category", 'user', "heading", "status",
                  "tags","expire"]

    def create(self, validated_data):
        return ForeCast.objects.create(**validated_data)


class GetForecastSerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = ForeCast
        fields = ["user_id"]


class PlaceBetSerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    forecast_id = serializers.IntegerField()
    points = serializers.IntegerField()
    bet_id = serializers.IntegerField()

    class Meta:
        model = ForeCast
        fields = ["user_id", "forecast_id", "points", "bet_id"]


class GetPlayedForecastSerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Betting
        fields = ["user_id"]


class ReferralCodeSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField()
    user_joined = serializers.IntegerField()

    class Meta:
        model = Betting
        fields = ["referral_code", "user_joined"]


class UserInterestSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    interest = serializers.CharField(required=True)

    class Meta:
        model = UserInterest
        fields = ["user_id", "interest"]


class ResultSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = ForeCast
        fields = ["user_id"]


class AuthenticationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Authentication
        fields = ["user_id"]


class AdvertisementPointsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = AdvertisementPoints
        fields = ["user_id"]