from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    current_revision = models.ForeignKey('Revision', related_name='current_revision', blank=True, null=True)

    def get_absolute_url(self):
        return "/" + self.slug + "/"

    def __unicode__(self):
        return self.title


class Revision(models.Model):
    text = models.TextField()
    comment = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    parent = models.ForeignKey('self', null=True)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return "/revision/%s/" % self.id

    def __unicode__(self):
        return str(self.id)



