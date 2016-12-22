from __future__ import unicode_literals
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from tinymce_4.fields import TinyMCEModelField
from taggit.managers import TaggableManager
from django.db import models

fs = FileSystemStorage(location=settings.STATIC_ROOT_ARTICLES)

# A SUPPRIMER
def content_file_name(instance, filename):
    return 'articles/images/header/article/'.join([instance.link, filename])


@python_2_unicode_compatible
class Category(models.Model):
    title = models.CharField(_('Titre'), max_length=20)
    link = models.SlugField(_('Lien'), max_length=20)
    image = models.ImageField(_('Background photo'), upload_to='articles/images/header/category', storage=fs,
                              default='articles/images/header/category/default.jpg')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(_('Titre'), max_length=200)
    subhead = models.TextField(_('Bandeau'), null=True, blank=True)
    body = TinyMCEModelField(_('Article'))
    image = models.ImageField(_('Background photo'), upload_to='articles/images/header/article/', storage=fs,
                              default='articles/images/header/article/default.jpg')
    video = models.SlugField(_('Background video'), max_length=20, null=True, blank=True, default='header')
    use_video = models.BooleanField(_('Utiliser video?'), default=False)
    link = models.SlugField(_('Lien'), max_length=200, unique=True, null=True, blank=True)
    date = models.DateTimeField(_('Date de publication'), auto_now_add=True)

    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.link = link = slugify(self.title)
            counter = 1
            while self.__class__.objects.filter(link=self.link).exists():
                self.link = '{0}-{1}'.format(link, counter)
            counter += 1
        return super(Article, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Comment(models.Model):
    """
    Comment model for the articles's pages.
    """
    article = models.ForeignKey(Article)
    author = models.ForeignKey(User)
    date = models.DateTimeField(_('Date de publication'), auto_now_add=True)
    text = models.TextField(_('Commentaire'), max_length=480)

    def __str__(self):
        """
        Make the 'Comment.article' readable by returning its title text when called.
        :return: article, the name of the article where the comment is posted (str).
        """
        return self.article.name
