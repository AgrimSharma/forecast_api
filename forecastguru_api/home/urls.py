from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/', login_user, name='login'),
    url(r'^referral_code/', referral_code, name='referral_code'),
    url(r'^check_referral/', check_referral, name='check_referral'),
    url(r'^interest_select/', interest, name='interest_select'),
    url(r'^live_forecast/', live_forecast, name='live_forecast'),
    url(r'^interest_skip/', interest_skip, name='interest_skip'),
    url(r'^', index, name='index'),

]

# handler404 = e_handler404
# handler500 = e_handler500