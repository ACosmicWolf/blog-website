from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
import datetime


from .models import User,Blog

from . import utils
# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    return render(request,"blogs/home.html",{"cards":blogs})


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
        title = request.POST['title']
        content = request.POST['content']
        current_user = request.user
        model = Blog(
            title=title,
            date_added=datetime.datetime.now(),
            author=current_user
        )
        model.save()
        utils.save_entry(title,content)
        return render(request,"blogs/home.html",{"message":"Blog Has Been Saved."})
    else:
        return render(request,'blogs/createblog.html')

def viewblog(request, blog):
    blog = Blog.objects.get(id=blog)
    title = blog.title
    print(blog.views)
    blog.views=blog.views+1
    blog.save()
    content = utils.get_entry(title)
    print(content)
    return render(request,"blogs/viewblog.html",{"title":title,"content":content})

def userprofile(request, username):
    user = User.objects.get(username=username)
    try:
        posts = Blog.objects.filter(author=user)
    except:
        posts = None
    return render(request,"blogs/users.html",{"user":user,"posts":posts})