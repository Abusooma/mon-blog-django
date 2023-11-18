from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Titre')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    create_on = models.DateField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False, verbose_name='Publié')
    content = models.TextField(blank=True, verbose_name='contenu')
    thumbnail = models.ImageField(blank=True, upload_to='blog')

    class Meta:
        ordering = ['-create_on']
        verbose_name = 'Article'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_author(self):
        return self.author.username if self.author else "Auteur inconnu"




