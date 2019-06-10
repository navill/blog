from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from tagging.fields import TagField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):  # -> string
        return self.name + str(f'&게시글 수: {Post.objects.all().count()}')


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=100)
    text = RichTextUploadingField()
    tag = TagField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        # detail/<int:pk>/
        return reverse('blog:detail', args=[self.id])
