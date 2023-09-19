from django.contrib import admin
from .models import News,Category,Contact,Comment
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_time', 'slug', 'status']
    list_filter = ['published_time', 'created_time', 'status']
    prepopulated_fields = { "slug": ('title', )}
    date_hierarchy = 'published_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'published_time']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id' ,'name']



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time',]
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'active_comments']
    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def active_comments(self, request, queryset):
        queryset.update(active=True)