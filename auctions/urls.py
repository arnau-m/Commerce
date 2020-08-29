from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("viewCategory/<str:category>", views.viewCategory, name="viewCategory")
]
