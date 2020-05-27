from django.conf import settings
from django.urls import re_path
from rest_framework.routers import DefaultRouter, SimpleRouter

from football_opinionated.users.api.views import UserViewSet, UserFollowView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns =[
    re_path(r'^users/(?P<username>[\w-]+)/follow$', UserFollowView.as_view(), name="follow"),
] + router.urls
