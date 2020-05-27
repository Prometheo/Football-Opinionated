from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedIdentityField
from rest_framework.fields import CurrentUserDefault
from ..models import Question
from Comment.models import Comment
from Comment.api.serializers import CommentSerializer


question_detail_url = HyperlinkedIdentityField(
        view_name='questions-api:detail',
        lookup_field='uuid'
        )

class QuestionListSerializer(ModelSerializer):
    user = SerializerMethodField()
    url = question_detail_url
    Answers = SerializerMethodField()
    likes = SerializerMethodField()
    class Meta:
        model = Question
        fields = [
            'id',
            'url',
            'uuid',
            'content',
            'created_on',
            'image',
            'user',
            'slug',
            'Answers',
            'draft',
            'likes',
        ]

    def get_user(self, obj):
        return obj.user.username


    def get_Answers(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = c_qs.count()
        return comments

    def get_likes(self, obj):
        return obj.num_of_likes


class QuestionDetailSerializer(ModelSerializer):
    #url = question_detail_url
    comments = SerializerMethodField()
    likes = SerializerMethodField()
    liked = SerializerMethodField()
    class Meta:
        model = Question
        fields = [
            #'url',
            'id',
            'uuid',
            'content',
            'likes',
            'liked',
            'created_on',
            'comments',
            'image',

        ]
    
    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments

    def get_likes(self, obj):
        return obj.num_of_likes

    def get_liked(self, obj):
        user = self.context['request'].user
        print(self.context['request'].user)
        print(self.context)
        if user in obj.liked_by.all():
            return True
        return False

class QuestionCreateSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'content',
            'image',
            'draft',
            #'liked_by',
        ]

# class QuestionEditSerializer(ModelSerializer):
#     class Meta:
#         model = Question
#         fields = [
#             'content',
#             'image',
#         ]
class QuestionLikeSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'liked_by'
        ]
