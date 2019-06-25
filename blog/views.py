from django.shortcuts import render
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Post, Category

from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


class PostList(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = 'post_object_list'
    paginate_by = 2  # 한 페이지당 요수 갯수

    def get_context_data(self, **kwargs):
        context_data = super(PostList, self).get_context_data(**kwargs)
        # context_data['categories'] = Category.objects.filter(parent_category=None)
        context_data['categories'] = Category.objects.all()
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'category_slug' in self.kwargs:
            try:
                category = Category.objects.get(slug=self.kwargs['category_slug'])
                queryset = queryset.filter(category=category)
            except:
                pass
        return queryset

    def dispatch(self, request, *args, **kwargs):
        post_objects = Post.objects.all()
        paginator = Paginator(post_objects, self.paginate_by)
        context_data = {}
        if request.method == 'GET':
            self.page = request.GET.get('page')
            if self.page is None or int(self.page) < 1:
                self.page = 1
            try:
                list_object = paginator.page(self.page)
            except PageNotAnInteger:
                list_object = paginator.page(1)
            except EmptyPage:
                list_object = paginator.page(paginator.num_pages)
            context_data.update(
                {'object_list': list_object})
            return render(request, 'blog/post_list.html', context_data)
        return super(PostList, self).dispatch(request, *args, **kwargs)


"""
setup -> dispatch -> get_object -> get_queryset -> get_context_data -> render_to_response
이를 직접 구현하는 것이 함수형 뷰
"""


class PostUpdate(UpdateView):
    model = Post
    fields = ['category', 'title', 'text']
    template_name = "blog/post_update.html"
    # success_url = '/'
    # create에서 form_valid가 실행되어있기 때문에 overriding이 필요하지 않음


"""
setup -> dispatch -> get -> post -> get_object -> get_context_data -> rendoer_to_response
"""


# start Create
class PostCreate(CreateView):
    model = Post
    fields = ['category', 'author', 'title', 'text']
    # appname/model_form.html (update & create)
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.author.username = self.request.user.id
        return super().form_valid(form)


"""
setup -> dispatch -> get -> post -> get_context_data -> rendoer_to_response
"""

from django.urls import reverse_lazy


class PostDelete(DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy('blog:list')  # reverse_lazy(app_name:urls_name)


class PostDetail(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class CategoryList(ListView):
    model = Category
    template_name = "blog/category_list.html"
    context_object_name = "category_object_list"


class AboutView(TemplateView):
    template_name = "blog/about.html"


from django.core.mail import EmailMessage
from django.conf import settings


class ContactView(TemplateView):
    template_name = "blog/contact.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = request.POST.copy()
            name = data.get('name')
            email = data.get('email')
            phone_number = data.get('phone')
            message = data.get('message')
            text = f'from : {email} \nmessage : {message}'
            email_object = EmailMessage((name, phone_number), text,
                                        to=[settings.EMAIL_HOST_USER])
            print(email_object.send())
            return render(request, 'blog/contact_success.html')
        return render(request, 'blog/contact.html')


from tagging.views import TaggedObjectList


class PostTaggedObjectList(TaggedObjectList):
    model = Post
    allow_empty = True
    template_name = 'post/post_list.html'

#
# from django.views.generic import TemplateView
#
#
# class TagList(TemplateView):
#     template_name = 'post/tag_list.html'
