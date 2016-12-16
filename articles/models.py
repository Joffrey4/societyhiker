from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from django.db import models


@python_2_unicode_compatible
class Category(models.Model):
    title = models.CharField(max_length=20)
    link = models.SlugField(max_length=20)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=200)
    subhead = models.TextField(null=True, blank=True)
    body = HTMLField()
    image = models.ImageField(upload_to='articles/images/header', default='articles/images/header/default.jpg')
    link = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slug = slugify(self.title)
            counter = 1
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = '{0}-{1}'.format(slug, counter)
            counter += 1
        return super(Article, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Comment(models.Model):
    """
    Comment model for the articles's pages.
    """
    article = models.ForeignKey(Article)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=480)

    def __str__(self):
        """
        Make the 'Comment.article' readable by returning its title text when called.
        :return: article, the name of the article where the comment is posted (str).
        """
        return self.article.name
