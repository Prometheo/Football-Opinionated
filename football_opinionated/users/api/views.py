from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .permissions import IsOWnerOrReadOnly
from .serializers import UserSerializer
User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = [IsOWnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(username=self.request.user.username)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class UserFollowView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, format=None):
        #quest_obj = Question.objects.get(uuid=uuid)
        #current_user, created = User.objects.get_or_create(username=username)
        try:
            to_person= User.objects.get(username=username)
        except:
            to_person = None
        
        message = "Not allowed"
        if self.request.user.is_authenticated and to_person:
            following = User.objects.follow_toggle(self.request.user, to_person)
            return Response({'message':following})
        return Response({'message':message}, status=400)


class UserSearchView(views.APIView):

    def get(self, request):
        keyword = self.request.GET.get('keyword')
        results = User.objects.filter(username__icontains=keyword)
        results = UserSerializer(results, many=True, context={'request': request}).data
        if len(results)>0:
            return Response(data=results)
        return Response({'message': 'no matching users where found'})
