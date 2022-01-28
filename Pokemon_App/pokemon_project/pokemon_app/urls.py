from django.urls import path
from . import views


urlpatterns = [
    path('', views.pokemon),
    path('login_registration', views.login_registration),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('home', views.main_landing),
    path('account/<int:user_id>/view', views.account_main),
    path('account/<int:user_id>/battle', views.battle),
    path('account/<int:user_id>/leaderboards', views.leaderboard),

]