from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import User, Post, Like, Author
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core import serializers
from django.core.serializers import serialize
from rest_framework import viewsets
from .serializers import PostSerializer, LikeSerializer, UserSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404



def index(request):

    post_form = PostForm()
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        addpost(request)
    return render(request, "network/index.html", {'post_form': post_form})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def addpost(request):
    
    form = PostForm(request.POST)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created = timezone.now()
            instance.author = request.user
            form = instance.save()
            return redirect('allposts')

    else:
        form = PostForm()
    return render(request, "network/index.html", {"form": form})


# view for all posts 


def allposts(request):

    user = request.user

    post_form = PostForm()
    allposts = Post.objects.all()

    if not request.user.is_authenticated:
        return redirect('login')
    
    for post in allposts:
        post.liked = Like.objects.filter(who_liked_it=user, post=post).exists()
        post.save()
    
    p = Paginator(allposts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    
    if request.method == 'POST':
        addpost(request)

    args = { 'post_form': post_form, 'page_obj': page_obj, 'user': user }

    return render(request, "network/allposts.html", args)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint  allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint  allows groups to be viewed or edited.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint  allows groups to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


def postpages(request):
    allposts = Post.objects.all()
    paginator = Paginator(allposts, 10)
    page = request.GET.get('page')
    try:
        allposts = paginator.page(page)
    except PageNotAnInteger:
        allposts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        allposts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'network/list_ajax.html', {'section': 'allposts', 'allposts': allposts })
    return render(request, 'network/allposts.html', {'section': 'allposts', 'allposts': allposts })


@login_required
def user_list(request, author):
    author = User.objects.get(id=author)
    posts = Post.objects.filter(author=author)
    user = request.user

    button = "Follow" if Author.objects.filter(user_from=request.user, user_to=author).count() == 0 else "Unfollow"

    if request.method == "POST":
        if request.POST["button"] == "Follow":
            button = "Unfollow"
            Author.objects.create(user_from=request.user, user_to=author)
        else:
            button = "Follow"
            Author.objects.get(user_from=request.user, user_to=author).delete()

    for post in posts:
        post.liked = Like.objects.filter(who_liked_it=user, post=post).exists()
        post.save()

    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    args = { 
        "followers": Author.objects.filter(user_to=author).count(), 
        "following": Author.objects.filter(user_from=author).count(), 
        "page_obj": page_obj, 
        "author": author,
        "button": button,
        "user":user
    }

    return render(request, 'network/user/list.html', args)



@login_required
def following(request):
    user = request.user

    following_posts = Author.objects.filter(user_from=request.user).values('user_to_id')

    posts = Post.objects.filter(author__in=following_posts)

    for post in posts:
        post.liked = Like.objects.filter(who_liked_it=user, post=post).exists()
        post.save()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    post_form = PostForm()

    if request.method == 'POST':
        addpost(request)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "post_form": post_form, 
        "user": user
    })


def liketoggle(request, post_id):

    post = Post.objects.get(id=post_id)
    user = request.user

    # like_check = Like.objects.filter(who_liked_it=user, post=post).exists()

    if request.method == 'POST':
        Like.objects.filter(who_liked_it=user, post=post).delete() if Like.objects.filter(who_liked_it=user, post=post).exists() else Like.objects.create(who_liked_it=user, post=post)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)
    


    
