from django.urls import path
from . import views

app_name = "links"

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("", views.home, name="home"),
    path("url_check/", views.urlCheck, name="schedule"),
    path("manage_cat_tags/", views.manageCatTags, name="manage_cat_tags"),
    path("add_link/", views.addLink, name="add_link"),
    path("add_cat/", views.addCategory, name="add_cat"),
    path("add_tag/", views.addTag, name="add_tag"),
    path("update_link/<str:pk>/", views.updateLink, name="update_link"),
    path("update_cat/<str:pk>/", views.updateCategory, name="update_cat"),
    path("update_tag/<str:pk>/", views.updateTag, name="update_tag"),
    path("delete_link/<str:pk>/", views.deleteLink, name="delete_link"),
    path("delete_cat/<str:pk>/", views.deleteCategory, name="delete_cat"),
    path("delete_tag/<str:pk>/", views.deleteTag, name="delete_tag"),
    path("cli/", views.commandLineInterface, name="cli"),
]
