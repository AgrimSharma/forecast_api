from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/', login_user, name='login'),
    url(r'^', home, name='home'),

]

# handler404 = e_handler404
# handler500 = e_handler500