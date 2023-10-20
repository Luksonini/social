from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.serializers import serialize

from .models import User, PostModel
from rest_framework import serializers
from rest_framework.generics import ListAPIView


def index(request):
    return render(request, "network/index.html")

def custom_comment_serializer(posts):
    serialized_data = []
    
    for post in posts:
        serialized_data.append({
            'author_id': post.author.id,
            'author_username': post.author.username,
            'body': post.body,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return serialized_data


class PostModelSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True) 
    profile_image = serializers.ImageField(source='author.profile_picture', read_only=True)

    class Meta:
        model = PostModel
        fields = ('author', 'author_username', 'body', 'created_at', 'profile_image')


class PostListView(ListAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostModelSerializer


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
