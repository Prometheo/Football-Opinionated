from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
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

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    slug = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CommentManager()
    #question_answered = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_on"]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        db_table = "Comment_to_Questions"


    def __str__(self):
        return self.content