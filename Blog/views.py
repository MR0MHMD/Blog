# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login, logout
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# from django.views.generic import ListView
# from django.http import HttpResponse
from django.db.models import Q
from .models import *
from .forms import *


# Create your views here.

def index(request):
    return render(request, 'blog/index.html')


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'blog/list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    form = CommentForm()
    comments = post.comments.filter(active=True)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                message=cd['message'],
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject']
            )
            return redirect('blog:post_list')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'forms/comment.html', context)


@login_required()
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(post=post, image_file=request.FILES['image1'])
            Image.objects.create(post=post, image_file=request.FILES['image2'])
            return redirect('blog:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form': form})


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (Post.published.annotate(
                sim_post_title=TrigramSimilarity('title', query),
                sim_post_desc=TrigramSimilarity('description', query),
                sim_image_title=TrigramSimilarity("images__title", query),
                sim_image_desc=TrigramSimilarity("images__description", query)).filter(
                Q(sim_post_title__gt=0.1) |
                Q(sim_post_desc__gt=0) |
                Q(sim_image_title__gt=0.1) |
                Q(sim_image_desc__gt=0)
            ))

    context = {
        'query': query,
        'results': results
    }
    return render(request, 'blog/search.html', context)


@login_required()
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    return render(request, 'blog/profile.html', {'posts': posts})


@login_required()
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        post.delete()
        return redirect('blog:profile')
    else:
        return render(request, 'forms/delete_post.html', {'post': post})


@login_required()
def delete_image(request, pk):
    image = get_object_or_404(Image, id=pk)
    image.delete()
    return redirect('blog:profile')


@login_required()
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(post=post, image_file=request.FILES['image1'])
            Image.objects.create(post=post, image_file=request.FILES['image2'])
            return redirect('blog:profile')
    else:
        form = CreatePostForm(instance=post)
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'forms/create_post.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required()
def edit_account(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        account_form = AccountEditForm(request.POST, request.FILES, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            return redirect("blog:profile")
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)
    context = {
        'user_form': user_form,
        'account_form': account_form
    }
    return render(request, 'registration/edit_account.html', context)


def profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    account = user.account
    posts = Post.published.filter(author=user)
    context = {
        'user': user,
        'account': account,
        'posts': posts
    }
    return render(request, 'blog/profile_detail.html', context)
