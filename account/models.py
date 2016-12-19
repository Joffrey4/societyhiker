from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(_('Pseudo'), max_length=20, blank=True)
    bio = models.TextField(_('Biographie'), blank=True)
    location = models.CharField(_('Lieu'), max_length=30, blank=True)
    birth_date = models.DateField(_('Date de naissance'), null=True, blank=True)
    picture = models.ImageField(_('Photo'), upload_to='account/images/profile', default='account/images/profile/default.jpg')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        """
        Make the 'Profile.nickname' readable by returning its nickname when called.
        :return: nickname, the nickname of the user.
        """
        return self.nickname
