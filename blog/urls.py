from django.urls import path, re_path
from .views import *

app_name = 'blog'

urlpatterns = [
    # as_view() : class 뷰를 function 사용될 때 사용된다.
    # path('', PostList.as_view(), name='list'),
    # path('', postList, name='list'),
    # path('', postList, name='list'),
    # re_path(r'^(?P<page_num>[0-9]+)*/{0,1}$', PostList.as_view(), name='list'),
    path('', PostList.as_view(), name='list'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('create/', PostCreate.as_view(), name='create'),
    path('delete/<int:pk>/', PostDelete.as_view(), name='delete'),
    path('update/<int:pk>/', PostUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', PostDetail.as_view(), name='detail'),
    path('category/<int:pk>/', CategoryList.as_view(), name='c_list'),
    path('tags/<tag>/', PostTaggedObjectList.as_view(), name='post_taggedlist'),
    # path('tags/', TagList.as_view(), name='tag_list'),
]
