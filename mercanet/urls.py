from django.urls import path

from mercanet import views

urlpatterns = [
    path("pay/", views.mercanet_request, name="pay"),
    path("auto/", views.mercanet_response, name="auto"),
]
