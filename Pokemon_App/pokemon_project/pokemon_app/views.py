
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Pokemon
from django.db import models
from django.contrib import messages
import requests
import bcrypt


# Create your views here.

def index(request):
    request.session.flush()
    return render(request, 'index.html')

def login_registration(request):
    return render(request, 'login_registration.html')


def main_landing(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id= request.session['user_id']),
    }
    return render(request,'home.html', context)

def register(request):
    if request.method == "GET":
        return redirect('/login_registration')

    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/login_registration')
    else:
        password = request.POST['password']

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            username = request.POST['username'],
            wins = 0,
            loses = 0,
            pokemon1 = '',
            pokemon2 = '',
            pokemon3 = '',
            password = pw_hash,

        )
        request.session['user_id'] = new_user.id
    return redirect('/home')

def login(request):
    if request.method == "GET":
        return redirect('/login_registration')


    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/login_registration')
    else:
        logged_user = User.objects.get(username = request.POST['username'])
        request.session['user_id'] = logged_user.id
        return redirect('/home')


def account_main(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/login_registration')

    user = User.objects.get(id= user_id)

    context = {
        "user": user,
    }
    return render(request,'account.html', context)


def logout(request):
    request.session.flush()
    return redirect('/login_registration')

#Battle Temp
def battle(request, user_id):
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=20').json()
    context = {'pokemon' : response['results']}
    return render(request, 'battle.html', context)

#Leaderboard Temp
def leaderboard(request, user_id):
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=20').json()
    context = {'pokemon' : response['results']}
    return render(request, 'leaderboard.html', context)


# Pokemon temp
def pokemon(request):
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=20').json()
    context = {'pokemon' : response['results']}
    return render(request, 'index.html', context)




