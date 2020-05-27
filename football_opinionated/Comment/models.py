import uuid as uuid_lib
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from football_opinionated.users.models import User
# Create your models here.

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None

    def like_toggle(self, user, Coment_obj):
        if user in Coment_obj.var_goal.all():
            is_liked = False
            Coment_obj.var_goal.remove(user)
        else:
            is_liked = True
            Coment_obj.var_goal.add(user)
        return is_liked

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    slug = models.SlugField()
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)
    draft = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CommentManager()
    var_goal = models.ManyToManyField(User, related_name='var_goal', blank=True)
    #question_answered = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_on"]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        db_table = "Comment_to_Questions"


    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('comments:detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.content[:45])
        super(Comment, self).save(*args, **kwargs)

    def replies(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    @property
    def num_of_goals(self):
        return self.var_goal.all().count()