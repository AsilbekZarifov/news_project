from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import Category,News,Contact
# Create your views here.
from .forms import Contactfrom


def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)
    context = {
        "news_list": news_list
    }

    return render(request, 'news/news_list.html', context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news":news
    }

    return render(request, 'news/news_detail.html',context)

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








