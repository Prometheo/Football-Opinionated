from django.urls import path, re_path
from .views import CommentList, CommentDetail, CommentCreate, LikeComment

app_name = 'Comment'

urlpatterns = [
    path("", CommentList.as_view(), name="comment-list"),
    re_path(r'^(?P<uuid>[\w-]+)/$', CommentDetail.as_view(), name="thread"),
    path("create", CommentCreate.as_view(), name="create"),
    re_path(r'^(?P<uuid>[\w-]+)/like$', LikeComment.as_view(), name="like"),
]