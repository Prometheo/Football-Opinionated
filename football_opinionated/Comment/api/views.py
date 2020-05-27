from rest_framework import generics, mixins, views
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from .serializers import CommentSerializer, CommentDetailSerializer, create_comment_serializer
from Comment.models import Comment
from Questions.api.permissions import IsOWnerOrReadOnly

class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'uuid'
    permission_classes = [IsOWnerOrReadOnly]


class CommentDetail(generics.RetrieveAPIView, DestroyModelMixin, UpdateModelMixin):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    lookup_field = 'uuid'
    permission_classes = [IsOWnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        coment = Comment.objects.get(uuid=self.kwargs['uuid'])
        if not coment.user == self.request.user:
            raise PermissionDenied("you can't edit someone's comment")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        coment = Comment.objects.get(uuid=self.kwargs['uuid'])
        if not coment.user == self.request.user:
            raise PermissionDenied("you can't delete someone's comment")
        return self.destroy(request, *args, **kwargs)

class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug =  self.request.GET.get("slug")
        print('req:', self.request)    
        print('GET:', self.request.GET)
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
                model_type=model_type, 
                slug=slug, 
                parent_id=parent_id,
                user=self.request.user
                )


class LikeComment(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid, format=None):
        quest_obj = Comment.objects.get(uuid=uuid)
        message = "Not allowed"
        if self.request.user.is_authenticated:
            liked = Comment.objects.like_toggle(request.user, quest_obj)
            return Response({'liked':liked})
        return Response({'message':message}, status=400)