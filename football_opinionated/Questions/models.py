import uuid as uuid_lib
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from football_opinionated.users.models import User
from Comment.models import Comment
# Create your models here.

class QuestionManager(models.Manager):
    def published(self):
        return super(QuestionManager, self).filter(draft=False)


    def like_toggle(self, user, Quest_obj):
        if user in Quest_obj.liked_by.all():
            is_liked = False
            Quest_obj.liked_by.remove(user)
        else:
            is_liked = True
            Quest_obj.liked_by.add(user)
        return is_liked

def upload_location(instance, filename):
    QuestionModel = instance.__class__
    path = QuestionModel.objects.order_by('id').last().id + 1
    return f'{path}/{filename}'




class Question(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="Author", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    objects = QuestionManager()
    tags = TaggableManager()
    liked_by = models.ManyToManyField(User, related_name='liked_by', blank=True)
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

    def get_absolute_url(self):
        return reverse('question:detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.content[:25])
        super(Question, self).save(*args, **kwargs)


    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def num_of_likes(self):
        return self.liked_by.all().count()