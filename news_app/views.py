from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView,CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from hitcount.utils import get_hitcount_model

from .models import Category,News,Contact
# Create your views here.
from .forms import Contactfrom,CommentForm
from news_project.custom_permissions import OnlyLoggedSuperUser
from hitcount.views import HitCountDetailView, HitCountMixin


def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)
    context = {
        "news_list": news_list
    }

    return render(request, 'news/news_list.html', context)



def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    new_comment = None

    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi komment obyektini yaratamiz lekn DB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # ma'lumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        'comments': comments,
        'new_comment': new_comment,
        'comment_count': comment_count,
        'comment_form': comment_form
    }
    return render(request, 'news/news_detail.html', context)



# bu funksiya orqali yozilgani
# def HomePageview(request):
#     news_list = News.objects.filter(status=News.Status.Published).order_by('-published_time')[:5]
#     categories = Category.objects.all()
#     local_one = News.objects.filter(status=News.Status.Published).filter(category__name="Mahalliy").order_by("-published_time")[0]
#     local_news = News.objects.filter(status=News.Status.Published).filter(category__name="Mahalliy").order_by("-published_time")[1:6]
#
#     context = {
#         'news_list':news_list,
#         'categories':categories,
#         'local_one':local_one,
#         'local_news':local_news
#     }
#     return render(request, 'news/home.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.objects.filter(status=News.Status.Published).order_by('-published_time')[:5]
        context['local_news'] = News.objects.filter(status=News.Status.Published).filter(category__name="Mahalliy").order_by("-published_time")[1:6]
        context['foreign_news'] = News.objects.filter(status=News.Status.Published).filter(category__name="Xorij").order_by("-published_time")[1:6]
        context['sport_news'] = News.objects.filter(status=News.Status.Published).filter(category__name="Sport").order_by("-published_time")[1:6]
        context['tex_news'] = News.objects.filter(status=News.Status.Published).filter(category__name="Texnologiya").order_by("-published_time")[1:6]

        return context


# def contactPageview(request):
#     print(request.POST)
#     form = Contactfrom(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Biz bilan bog'langaningiz uchun raxmat!")
#
#     context = {
#         "form":form
#     }
#
#     return render(request, 'news/contact.html', context)



class ContanctPageView(TemplateView):
    template_name = 'news/conctact.html'


    def get(self, request, *args, **kwargs):
        form = Contactfrom

        context = {
                 "form":form
             }
        return render(request,'news/contact.html', context)


    def post(self, request, *args, **kwargs):
        form = Contactfrom(request.POST)

        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun raxmat!")

        context = {
            "form": form
        }

        return render(request, 'news/contact.html', context)



def Page404view(request):
    context = {

    }

    return render(request, 'news/404.html', context)


def aboutView(request):
    context = {

    }
    return render(request, 'news/contact.html', context)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = News.objects.filter(status=News.Status.Published).filter(category__name="Mahalliy")
        return news


class XorijNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'


    def get_queryset(self):
        news = News.objects.filter(status=News.Status.Published).filter(category__name="Xorij")
        return news



class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'


    def get_queryset(self):
        news = News.objects.filter(status=News.Status.Published).filter(category__name="Sport")
        return news



class TexnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologiya_yangiliklar'


    def get_queryset(self):
        news = News.objects.filter(status=News.Status.Published).filter(category__name="Texnologiya")
        return news


class UpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status',)
    template_name = 'crud/news_edit.html'



class NewsDeleteView(DeleteView, OnlyLoggedSuperUser):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreate(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'body', 'image', 'category', 'status', 'slug',)

@login_required()
@user_passes_test(lambda u:u.is_superuser) # super user ga faqat kurinadi
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }

    return render(request, 'pages/admin_page.html', context)

class SearchResultListView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)

        )