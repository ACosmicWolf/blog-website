from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createblog", views.createblog, name="createblog"),
    path("blogs/<int:blog>", views.viewblog, name="blogs"),
    path("users/<username>", views.userprofile, name="users"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
