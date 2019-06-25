from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from tagging.fields import TagField
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, db_index=True)
    # parent_category = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, default=None)

    def __str__(self):  # -> string
        return self.name + str(f'&게시글 수: {Post.objects.all().count()}')


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='category')
    # author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,  db_constraint=False, related_name='author')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, db_index=True)
    text = RichTextUploadingField()
    tag = TagField(blank=True)
    created = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        # detail/<int:pk>/
        return reverse('blog:detail', args=[self.id])
