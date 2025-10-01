from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter


# inlines

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ['title', 'description']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['name', 'body']


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish', 'status')
    ordering = ('-publish', 'title')
    list_filter = ('status', ('publish', JDateFieldListFilter))
    search_fields = ('title', 'description')
    raw_id_fields = ('author',)
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ('status',)
    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'phone')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'created', 'active')
    list_filter = ('active', ('created', JDateFieldListFilter), ('updated', JDateFieldListFilter))
    search_fields = ('name', 'body')
    list_editable = ('active',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'title', 'created')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'job', 'photo')
