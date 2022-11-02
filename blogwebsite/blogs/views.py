import re
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.template.defaultfilters import slugify

from blogs.forms import BlogForm
from .models import User,Blog
from . import utils

from django.db.models import Max

# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    try:
        mostViewed = Blog.objects.filter(views=Blog.objects.all().aggregate(Max('views')).get('views__max'))[0]
    except:
        mostViewed=None
    return render(request,"blogs/home.html",{"cards":blogs,"mostViewed":mostViewed})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "blogs/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "blogs/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "blogs/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "blogs/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "blogs/register.html")

def createblog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            utils.save_entry(form.cleaned_data['title'],form.cleaned_data['description'])
            newBlog = Blog(
                title = form.cleaned_data['title'],
                slug = slugify(form.cleaned_data['title']),
                author = request.user,
                tags = form.cleaned_data['tags']
            )
            newBlog.save()
            ## form.save(commit=False)
            ## TODO: Tags ##form.save_m2m()
        return redirect('/')
    else:
        form = BlogForm()
        return render(request,'blogs/createblog.html',{"form":form})

def viewblog(request, slug):
    blog = Blog.objects.get(slug=slug)
    title = blog.title
    blog.views=blog.views+1
    blog.save()
    content = utils.get_entry(title)
    return render(request,"blogs/viewblog.html",{"title":title,"content":content})

def userprofile(request, username):
    user = User.objects.get(username=username)
    try:
        posts = Blog.objects.filter(author=user)
    except:
        posts = None
    return render(request,"blogs/users.html",{"user":user,"posts":posts})

def search(request, query):
    try:
        result = Blog.objects.filter(title=query)
    except:
        result=None
    return render(request,"blogs/search.html",{"result":result})