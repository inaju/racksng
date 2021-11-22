from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("useraccount/", include("dj_rest_auth.urls")),
    # path("api-auth/", include("rest_framework.urls")),
    path("signup/", include("rest_auth.registration.urls")),
    path("userdetail/", UserDetailList.as_view()),
    path("sendbtc/", send_btc_again),
    path("transactioninfo/", transaction_info),
]
