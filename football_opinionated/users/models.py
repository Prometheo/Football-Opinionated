from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _



class UserManager(UserManager):

    def follow_toggle(self, current_user, person):
        if Friendship.objects.filter(current_user=current_user, to_user=person).exists():
            Friendship.objects.filter(current_user=current_user, to_user=person).delete()
            message = "unfollowed"
        else:
            friendship, created = Friendship.objects.get_or_create(current_user=current_user, to_user=person)
            message = "started following"
        return message

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    location = models.CharField(_("location of user"), blank=True, max_length=50)
    country = models.CharField(_("user's country"), blank=True, max_length=50)
    state = models.CharField(_("user's state"), blank=True, max_length=50)
    fav_team = models.CharField(_("user's team"), blank=True, max_length=50)
    phone_num = models.CharField(_("phone number of user"), blank=True, max_length=25)
    friends= models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='followers')
    objects = UserManager()


    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Friendship(models.Model):
    current_user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    started_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{current_user} follows {to_user}'

def upload_location(instance, filename):
    ProfileModel = instance.__class__
    path = ProfileModel.user.username
    return f'"profile_pics"/{path}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(_("user's Bio"), blank=True, max_length=255)
    avatar = models.ImageField(default='default.png', upload_to=upload_location, blank=True)