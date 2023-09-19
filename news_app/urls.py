from django.urls import path
from .views import news_list,news_detail,HomePageView,ContanctPageView,Page404view,aboutView,\
    LocalNewsView, XorijNewsView, TexnologyNewsView, SportNewsView,UpdateView,NewsDeleteView,NewsCreate,\
admin_page_view,SearchResultListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_list, name="all_news_list"),
    path('contact-us/', ContanctPageView.as_view(), name="contact_page"),
    path('news/<slug>/edit/', UpdateView.as_view(), name='news_update'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('page404/', Page404view, name="404_page"),
    path('about/', aboutView, name="about_page"),
    path('news/<slug:news>/', news_detail, name="news_detail_page"),
    path('local-news/', LocalNewsView.as_view(), name="local_news_page"),
    path('foreign-news/', XorijNewsView.as_view(), name="foreign_news_page"),
    path('tex-news/', TexnologyNewsView.as_view(), name="tex_news_page"),
    path('sport-news/', SportNewsView.as_view(), name="sport_news_page"),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultListView.as_view(), name='search_results'),
]