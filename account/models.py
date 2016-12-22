from __future__ import unicode_literals
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

fs = FileSystemStorage(location=settings.STATIC_ROOT_ACCOUNT)


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(_('Prenom'), max_length=20, blank=True)
    surname = models.CharField(_('Nom de famille'), max_length=20, blank=True)
    link = models.SlugField(_('Lien'), max_length=20, unique=True, null=True, blank=True)
    bio = models.TextField(_('Biographie'), blank=True)
    location = models.CharField(_('Lieu'), max_length=30, blank=True)
    birth_date = models.DateField(_('Date de naissance'), null=True, blank=True)
    picture = models.ImageField(_('Image de profil'), upload_to='account/images/profile', storage=fs,
                                default='account/images/profile/default.jpg')
    cover = models.ImageField(_('Image de couverture'), upload_to='account/images/cover',
                                default='account/images/cover/default.jpg')

    def save(self, *args, **kwargs):
        if not self.id:
            self.link = link = slugify(self.firstname)
            counter = 1
            while self.__class__.objects.filter(link=self.link).exists():
                self.link = '{0}-{1}'.format(link, counter)
            counter += 1
        return super(Profile, self).save(*args, **kwargs)

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
        return self.firstname + self.surname
