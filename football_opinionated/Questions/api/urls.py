from django.urls import path, re_path
from .views import QuestionList, QuestionDetail, QuestionCreate, QuestionEdit, QuestionDelete, LikeQuestion

app_name = 'Questions'

urlpatterns = [
    path("", QuestionList.as_view(), name="question-list"),
    re_path(r'^(?P<uuid>[\w-]+)/$', QuestionDetail.as_view(), name="detail"),
    path("create", QuestionCreate.as_view(), name="create"),
    re_path(r'^(?P<uuid>[\w-]+)/edit$', QuestionEdit.as_view(), name="edit"),
    re_path(r'^(?P<uuid>[\w-]+)/delete$', QuestionDelete.as_view(), name="delete"),
    re_path(r'^(?P<uuid>[\w-]+)/like$', LikeQuestion.as_view(), name="like"),
]