from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^main_login/', main_login, name='main_login'),
    url(r'^login_user/', login_user, name='login_user'),
    url(r'^referral_code/', referral_code, name='referral_code'),
    url(r'^check_referral/', check_referral, name='check_referral'),
    url(r'^interest_select/', interest, name='interest_select'),
    url(r'^live_forecast/', live_forecast, name='live_forecast'),
    url(r'^interest_skip/', interest_skip, name='interest_skip'),
    url(r'^create_forecast/', create_forecast, name='create_forecast'),
    url(r'^get_sub_cat/', get_sub_cat, name='get_sub_cat'),
    url(r'^get_sub_source/', get_sub_source, name='get_sub_source'),
    url(r'^bet_save/', bet_post, name='bet_save'),
    url(r'^notification/', notification, name='notification'),
    url(r'^get_forecast/', get_forecast, name='get_forecast'),
    url(r'^forecast/(?P<userid>\d+)/$', betting, name='betting'),
    url(r'^result_save/', result_save, name='result_save'),
    url(r'^terms_and_conditions/', terms, name="terms"),
    url(r'^profile/', profile, name="user_profile"),
    url(r'^refer_and_earn/', refer_earn, name="refer_and_earn"),
    url(r'^earn_points/', earn_points, name="earn_points"),
    url(r'^redeem_points/', redeem_points, name="redeem_points"),
    url(r'^faqs/', faq, name="faq"),
    url(r'^privacy_policy/', privacy, name="privacy_policy"),
    url(r'^import_csv/', import_csv, name="import_csv"),
    url(r'^closed_status/', update_close_status, name="closed_status"),
    url(r'^thank_you/', thank_you, name='thank_you'),
    url(r'^trending/', trending_forecast, name='trending'),
    url(r'^result_declared/', forecast_result, name='forecast_result'),
    url(r'^my_result/', result_not_declared, name='result_not_declared'),
    url(r'^my_forecast/', my_forecast, name='my_forecast'),
    url(r'^private/', my_forecast_private, name='private'),
    url(r'^logout_user/', logout_view, name='logout_user'),
    url(r'^search_result/', search_result, name='search_result'),
    url(r'^category/', category, name='category'),
    url(r'^category_search/(?P<userid>\d+)/$', category_search, name='category_search'),
    url(r'^sub_category_data/(?P<userid>\d+)/$', sub_category_data, name='sub_category_data'),
    url(r'^payment/', payment, name='payment'),
    url(r'^send_notification_user/', send_notification_user, name='send_notification_user'),
    url(r'^private_subscribe/', private_subscribe, name="private_subscribe"),
    url(r'^send_notification_all/', send_notification_all, name="send_notification_all"),
    url(r'^notif/', test_notif, name='notif'),
    url(r'^response/', response, name='response'),
    url(r'^notif_user/', save_user_id, name='notification_user'),
    # url(r'^login_facebook/', login_facebook, name='login_facebook'),
    url(r'^', index, name='index'),

]

# handler404 = e_handler404
# handler500 = e_handler500