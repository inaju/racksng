from django.contrib import admin
from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("useraccount/", include("dj_rest_auth.urls")),
    # path("api-auth/", include("rest_framework.urls")),
    path("signup/", include("rest_auth.registration.urls")),
    path("sendbtc/", send_btc_again),
    path("transactioninfo/", transaction_info),
]
