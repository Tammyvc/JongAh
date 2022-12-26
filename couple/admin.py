from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_time')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_time')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner','category', '标签', 'status', 'desc', 'created_time']
    search_fields = ['title']
    list_filter = ['category','created_time']
    list_per_page = 20

    def 标签(self, instance):
        return [tag.name for tag in instance.tags.all()]

    filter_horizontal = ('tags',)




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'email', 'status', 'created_time')
