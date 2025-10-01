from django import template

from ..models import Post, Comment
from django.db.models import Count, Max, Min
from markdown import markdown
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def last_post_date():
    return Post.published.last().publish


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    return {'l_posts': l_posts}


@register.simple_tag()
def most_popular_posts(count=4):
    return Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


@register.simple_tag()
def max_reading_time(count=1):
    return Post.published.annotate(max_time=Max('reading_time')).order_by("-reading_time")[:count]


@register.simple_tag()
def min_reading_time(count=1):
    return Post.published.annotate(min_time=Min('reading_time')).order_by("reading_time")[:count]
