from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/', login, name='login'),

]

# handler404 = e_handler404
# handler500 = e_handler500