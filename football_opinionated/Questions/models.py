from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from football_opinionated.users.models import User
from Comment.models import Comment
# Create your models here.

class QuestionManager(models.Manager):
    def published(self):
        return super(QuestionManager, self).filter(draft=False)


def upload_location(instance, filename):
    QuestionModel = instance.__class__
    path = QuestionModel.objects.order_by('id').last().id + 1
    return f'{path}/{filename}'


class Question(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="Author", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField()
    updated_on = models.DateTimeField(auto_now=True)
    objects = QuestionManager()
    tags = TaggableManager()
    # likes = models.IntegerField(default=0)
    # shares = models.IntegerField(default=0)
    # down_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ["created_on"]
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        db_table = "Question_table"

    def __str__(self):
        return self.slug

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs