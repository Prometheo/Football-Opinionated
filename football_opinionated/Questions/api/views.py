from rest_framework import generics, mixins, views
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import QuestionListSerializer, QuestionDetailSerializer, QuestionCreateSerializer, QuestionLikeSerializer
from Questions.models import Question
from .permissions import IsOWnerOrReadOnly

class QuestionList(generics.ListAPIView):
    queryset = Question.objects.published()
    serializer_class = QuestionListSerializer
    lookup_field = 'uuid'
    permission_classes = [IsOWnerOrReadOnly]


class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    lookup_field = 'uuid'
    permission_classes = [IsOWnerOrReadOnly]


class QuestionCreate(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionEdit(generics.RetrieveUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    lookup_field = 'uuid'

    def perform_update(self, serializer):
        quest = Question.objects.get(uuid=self.kwargs['uuid'])
        if not quest.user == self.request.user:
            raise PermissionDenied("you can't edit this question")
        serializer.save(user=self.request.user)
        

class QuestionDelete(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    lookup_field = 'uuid'
    permission_classes = [IsOWnerOrReadOnly]
    
    
class LikeQuestion(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid, format=None):
        quest_obj = Question.objects.get(uuid=uuid)
        message = "Not allowed"
        if self.request.user.is_authenticated:
            liked = Question.objects.like_toggle(request.user, quest_obj)
            return Response({'liked':liked})
        return Response({'message':message}, status=400)
    