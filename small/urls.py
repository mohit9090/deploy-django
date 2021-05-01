from django.urls import path
from . import views

app_name = "small"

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('article/', views.articlePage, name="article"),
    path('page-1/', views.page1, name="page1"),
    path('page-2/', views.page2, name="page2"),
    path('page-3/', views.page3, name="page3"),
    path('page-4/', views.page4, name="page4"),
    path('page-5/', views.page5, name="page5"),
    path('page-6/', views.page6, name="page6"),
    path('page-7/', views.page7, name="page7"),
]
