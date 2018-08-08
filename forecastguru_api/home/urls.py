from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/', login_user, name='login'),
    url(r'^referral_code/', referral_code, name='referral_code'),
    url(r'^check_referral/', check_referral, name='check_referral'),
    url(r'^interest_select/', interest, name='interest_select'),
    url(r'^live_forecast/', live_forecast, name='live_forecast'),
    url(r'^interest_skip/', interest_skip, name='interest_skip'),
    url(r'^create_forecast/', create_forecast, name='create_forecast'),
    url(r'^get_sub_cat/', get_sub_cat, name='get_sub_cat'),
    url(r'^get_sub_source/', get_sub_source, name='get_sub_source'),
    url(r'^bet_save/', bet_post, name='bet_save'),
    url(r'^get_forecast/', get_forecast, name='get_forecast'),
    url(r'^forecast/(?P<userid>\d+)/$', betting, name='betting'),
    url(r'^result_save/', result_save, name='result_save'),

    url(r'^', index, name='index'),

]

# handler404 = e_handler404
# handler500 = e_handler500