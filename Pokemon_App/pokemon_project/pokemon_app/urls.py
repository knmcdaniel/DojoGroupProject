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
    path('account/change/<int:slot>/<str:pokemon>', views.changePrimary),
    path('account/<int:user_id>/battle', views.battle),
    path('battle/<str:ability>', views.combat),
    path('account/<int:user_id>/battle/aiCombat', views.aiCombat),
    path('account/<int:user_id>/leaderboards', views.leaderboard),
    path('account/<int:user_id>/add_pokemon/<str:pokemon_name>', views.new_pokemon),
    path('new_pokemon/<str:pokemon_name>', views.new_pokemon),
    path('pokemon_modal/<str:pokemon_name>', views.pokemon_modal),
    path('account/<int:user_id>/battle/<str:pokemon>', views.changePokemon)
]