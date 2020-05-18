from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedIdentityField, ValidationError
from ..models import Comment

comment_detail_url = HyperlinkedIdentityField(
        view_name='comment-api:thread',
        lookup_field='uuid'
        )
    

def create_comment_serializer(model_type='question', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        
        class Meta:
            model = Comment
            fields = [
                'id',
                'parent',
                'content',
                'created_on',
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                    model_type, slug, content, main_user,
                    parent_obj=parent_obj,
                    )
            return comment

    return CommentCreateSerializer
        
class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    user = SerializerMethodField()
    #url = comment_detail_url
    content = SerializerMethodField()
    likes = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            #'url',
            'uuid',
            'content',
            'reply_count',
            'likes',
            'user',
            'created_on',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.replies().count()
        return 0

    def get_user(self, obj):
        return obj.user.username

    def get_content(self, obj):
        return (str(obj.content)[:13] + '.....')

    def get_likes(self, obj):
        return obj.num_of_goals

class CommentChildSerializer(ModelSerializer):
    #user = UserDetailSerializer(read_only=True)
    #url = comment_detail_url
    user = SerializerMethodField()
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'uuid',
            #'url',
            'user',
            'content',
            'reply_count',
            'created_on',
        ]

    def get_user(self, obj):
        return obj.user.username
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.replies().count()
        return 0


class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    likes = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'uuid',
            #'url',
            'user',
            'content',
            'likes',
            'reply_count',
            'replies',
            'created_on',
        ]
        read_only_fields = [
            'reply_count',
            'replies',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.replies().count()
        return 0

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.replies(), many=True).data
        return None

    def get_likes(self, obj):
        return obj.num_of_goals

    
class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model=Comment
        fields = [
            'var_goal'
        ]