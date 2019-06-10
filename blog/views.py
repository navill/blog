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

# Create your views here.
# import requests
# def naver_api(address):
#     naver_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" + address
#     custom_headers = {
#         "X-NCP-APIGW-API-KEY-ID": 'b4wnbq4cd7',
#         "X-NCP-APIGW-API-KEY": "8o4ERGCLrQgfFb9qoXRmJELLQBI6N3kHxUjELMXX"
#     }
#
#     # # requests of both API
#     naver_req = requests.get(naver_url, headers=custom_headers)
#     # result = list()
#     # jb_address = road_req.json()["results"]["juso"][0]['jibunAddr']
#     # rd_address = road_req.json()["results"]["juso"][0]['roadAddr']
#     # coord_lat = naver_req.json()["addresses"][0]["x"]
#     # coord_long = naver_req.json()["addresses"][0]["y"]
#     result = (
#               naver_req.json()["addresses"][0]["x"],
#               naver_req.json()["addresses"][0]["y"]
#               )
#     # result.append(road_req.json()["results"]["juso"][0]['jibunAddr'])
#     # result.append(road_req.json()["results"]["juso"][0]['roadAddr'])
#     # result.append(naver_req.json()["addresses"][0]["x"])
#     # result.append(naver_req.json()["addresses"][0]["y"])
#     return result



# start - View example
"""
class IndexView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'blog/test.thml')  # -> create http response


class JsonView(View):
    def get(self, *args, **kwargs):
        return JsonResponse({'Data': 'test'})

    def post(self, *args, **kwargs):
        return JsonResponse({'Data': 'test'})


def indexView(request):
    if request.method == "GET":
        return render(request, 'blog/test.html')


def jsonView(request):
    if request.method == "GET":
        return JsonResponse({"Data": "data"})
    elif request.method == "POST":
        return JsonResponse({"Data": "data"})


# end - example
"""
from django.core.paginator import Paginator
# start - List
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


class PostList(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = 'post_object_list'
    paginate_by = 3  # 한 페이지당 요수 갯수

    def dispatch(self, request, *args, **kwargs):
        post_objects = Post.objects.all()
        paginator = Paginator(post_objects, self.paginate_by)
        context_data = {}
        if request.method == 'GET':
            self.page = request.GET.get('page')
            if self.page is None or self.page < 1:
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
        # elif request.method == 'POST':
        #     # b = request.POST.get('search')
        #     search_keyword = request.POST.get('search', None)
        #     if search_keyword:
        #         q_title = Q(title__icontains=search_keyword)
        #         q_text = Q(text__icontains=search_keyword)
        #         filtered_objects = post_objects.filter(q_title | q_text)
        #         paginator = Paginator(filtered_objects, 3)
        #         if self.page < 1:
        #             self.page = 1
        #         list_object = paginator.page(1)
        #         context_data.update({'object_list': list_object})
        #         return render(request, 'blog/original_post_list.html', context_data)
        return super(PostList, self).dispatch(request, *args, **kwargs)


"""
setup -> dispatch -> get_object -> get_queryset -> get_context_data -> render_to_response
이를 직접 구현하는 것이 함수형 뷰
"""


# def postList(request, page_num):
#     page = page_num if page_num else 1
#     page = int(page)
#     # category_list = Category.objects.all()
#     queryset = Post.objects.all()  # -> class based view에서는 get_queryset()이 실행한다.
#     search_keyword = request.POST.get('search', request.GET.get('search', None))
#     # post(form에 입력된 search_keyword) & get(주소에 입력된 ?search={{search_keyword}})
#     context_data = {}
#     if search_keyword:
#         q_title = Q(title__icontains=search_keyword)
#         q_text = Q(text__icontains=search_keyword)
#         queryset = queryset.filter(q_title | q_text)
#         context_data.update({'search_keyword': search_keyword})
#     # print("search", search_keyword)
#     # page 번호 얻기
#     # paging 처리
#     paginator = Paginator(queryset, 3)  # object_list, per_page
#     page = paginator.page(page)  #
#     context_data.update(
#         {'object_list': page.object_list, 'page_obj': page_num, 'paginator': paginator, 'is_paginated': True, })
#     # 'category_list': category_list})
#     return render(request, 'blog/original_post_list.html', context_data)


# end - List

# start -update
class PostUpdate(UpdateView):
    model = Post
    fields = ['category', 'title', 'text']
    template_name = "blog/post_update.html"
    # success_url = '/'
    # create에서 form_valid가 실행되어있기 때문에 overriding이 필하지 않다.


"""
setup -> dispatch -> get -> post -> get_object -> get_context_data -> rendoer_to_response
"""


# # model factory를 이용한 update function view
# def postUpdate(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form_class = modelform_factory(Post, fields=['category', 'title', 'text'])
#     if request.method == "POST":
#         form = form_class(request.POST, instance=post)  # 2. 사용자가 입력한 정보는 request.POST, request.FILES에 포함된다.
#         if form.is_valid():
#             instance = form.save()
#             return redirect(instance)
#     elif request.method == "GET":
#         # 입력 폼 출력
#         form = form_class(instance=post)
#     return render(request, 'blog/post_create.html', {'form': form})


# end - update


# start Create
class PostCreate(CreateView):
    model = Post
    fields = ['category', 'author', 'title', 'text']
    # appname/model_form.html (update & create)
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


"""
setup -> dispatch -> get -> post -> get_context_data -> rendoer_to_response
"""
# # model factory를 이용한 create function view 만들기
# from django.forms import modelform_factory
#
#
# def postCreate(request):
#     form_class = modelform_factory(Post, fields=['category', 'title', ' text'])
#     if request.method == "POST":
#         form = form_class(request.POST)  # 2. 사용자가 입력한 정보는 request.POST, request.FILES에 포함된다.
#         form.instance.author_id = request.user.id  # login 되어있다는 가정
#         if form.is_valid():
#             instance = form.save()
#             return redirect(instance)
#     elif request.method == "GET":
#         # 입력 폼 출력
#         form = form_class()
#     return render(request, 'blog/post_create.html', {'form': form})

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
    # model = Category
    template_name = "blog/about.html"
    # naver_api("상원길 63")



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


from django.views.generic import TemplateView


class TagList(TemplateView):
    template_name = 'post/tag_list.html'
#
# import requests
# def naver_api(address):
#     naver_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" + address
#     custom_headers = {
#         "X-NCP-APIGW-API-KEY-ID": 'b4wnbq4cd7',
#         "X-NCP-APIGW-API-KEY": "8o4ERGCLrQgfFb9qoXRmJELLQBI6N3kHxUjELMXX"
#     }
#
#     # # requests of both API
#     naver_req = requests.get(naver_url, headers=custom_headers)
#     # result = list()
#     # jb_address = road_req.json()["results"]["juso"][0]['jibunAddr']
#     # rd_address = road_req.json()["results"]["juso"][0]['roadAddr']
#     # coord_lat = naver_req.json()["addresses"][0]["x"]
#     # coord_long = naver_req.json()["addresses"][0]["y"]
#     result = (
#               naver_req.json()["addresses"][0]["x"],
#               naver_req.json()["addresses"][0]["y"]
#               )
#     # result.append(road_req.json()["results"]["juso"][0]['jibunAddr'])
#     # result.append(road_req.json()["results"]["juso"][0]['roadAddr'])
#     # result.append(naver_req.json()["addresses"][0]["x"])
#     # result.append(naver_req.json()["addresses"][0]["y"])
#     return result