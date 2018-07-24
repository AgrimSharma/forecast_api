# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin


class AuthenticationAdmin(admin.ModelAdmin):
    list_display = ['email', 'facebook_id', 'last_login']


class DailyPointsFreeAdmin(admin.ModelAdmin):
    list_display = ['days', 'points']


class JoiningBonusAdmin(admin.ModelAdmin):
    pass


class ForecastAdmin(admin.ModelAdmin):
    list_display = ["forecast_heading", "forecast_category", "forecast_sub_category",
                    "forecast_user", "forecast_status", "forecast_expire"]

    def forecast_sub_category(self, obj):
        return obj.sub_category.name

    def forecast_category(self, obj):
        return obj.category.name

    def forecast_heading(self, obj):
        return obj.heading

    def forecast_user(self, obj):
        return obj.user.email

    def forecast_status(self, obj):
        return obj.status.name

    def forecast_expire(self, obj):
        return obj.expire


class StatusAdmin(admin.ModelAdmin):
    pass


class ApprovedAdmin(admin.ModelAdmin):
    pass


class WinningAdmin(admin.ModelAdmin):
    pass


class PrivateAdmin(admin.ModelAdmin):
    pass


class SubCategoryAdmin(admin.ModelAdmin):
    pass


class SubCatInline(admin.TabularInline):
    model = SubCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', "identifier"]
    ordering = ('identifier',)
    inlines = (SubCatInline,)


class AdvertisementPointsAdmin(admin.ModelAdmin):
    pass


class BettingAdmin(admin.ModelAdmin):
    list_display = ["user_email", 'forecast_heading', "forecast_category", "forecast_sub_category", "bet_for", "bet_against"]

    def user_email(self, obj):
        return obj.users.email

    def forecast_heading(self, obj):
        return obj.forecast.heading

    def forecast_category(self, obj):
        return obj.forecast.category.name

    def forecast_sub_category(self, obj):
        return obj.forecast.sub_category.name


class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ["user_email", 'referral_code']

    def user_email(self, obj):
        return obj.user_joined.email


class ReferralPointsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Authentication, AuthenticationAdmin)
admin.site.register(ReferralCodePoints, ReferralPointsAdmin)
admin.site.register(DailyFreePoints, DailyPointsFreeAdmin)
admin.site.register(ReferralCodeRegistered, ReferralCodeAdmin)
admin.site.register(Betting, BettingAdmin)
admin.site.register(JoiningPoints, JoiningBonusAdmin)
admin.site.register(ForeCast, ForecastAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Private, PrivateAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Winning, WinningAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Approved, ApprovedAdmin)
admin.site.register(AdvertisementPoints, AdvertisementPointsAdmin)


admin.site.site_title = 'ForeCast Guru'
admin.site.site_header = 'ForeCast Guru'
admin.site.index_title = 'Dashboard'
