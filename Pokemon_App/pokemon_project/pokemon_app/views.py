
import re
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Pokemon
from django.db import models
from django.contrib import messages
import requests
import bcrypt
import random


# Create your views here.

def index(request):
    request.session.flush()
    return render(request, 'index.html')

def login_registration(request):
    request.session.flush()
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
            pokemon1 = 'bulbasaur',
            pokemon2 = 'charmander',
            pokemon3 = 'squirtle',
            password = pw_hash,
        )

        # Make Bulbasaur for a new user
        Pokemon.objects.create(
            name = 'bulbasaur',
            api_id = 1,
            health = 100,
            wins = 0,
            type1 = 'grass',
            type2 = 'none',
            image = 'https://img.pokemondb.net/artwork/large/bulbasour.jpg',
            url = 'https://pokeapi.co/api/v2/pokemon/bulbasour',
            owner = new_user,
        )

        # Make charmander for a new user
        Pokemon.objects.create(
            name = 'charmander',
            api_id = 4,
            health = 100,
            wins = 0,
            type1 = 'fire',
            type2 = 'none',
            image = 'https://img.pokemondb.net/artwork/large/charmander.jpg',
            url = 'https://pokeapi.co/api/v2/pokemon/charmander',
            owner = new_user,
        )

        # Make squirtle for a new user
        Pokemon.objects.create(
            name = 'squirtle',
            api_id = 7,
            health = 100,
            wins = 0,
            type1 = 'water',
            type2 = 'none',
            image = 'https://img.pokemondb.net/artwork/large/squirtle.jpg',
            url = 'https://pokeapi.co/api/v2/pokemon/squirtle',
            owner = new_user,
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

    collected = Pokemon.objects.filter(owner = user)

    context = {
        "user": user,
        "collected" : collected,
    }
    return render(request,'account.html', context)


def logout(request):
    request.session.flush()
    return redirect('/login_registration')

#Create New Pokemon
def new_pokemon(request,user_id, pokemon_name):
    if 'user_id' not in request.session:
        return redirect('/login_registration')

    # Store user ID to save Pokemon to
    user = User.objects.get(id= user_id)

    # Verify the name/id is an accurate pokemon
    try:
        response = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(pokemon_name)).json()
    # If the name/id isn't accurate return the input and user to the error.html page
    except:
        context = {
            'bad_name' : pokemon_name,
        }
        return render(request, 'error.html', context)        


    if len(response['types']) == 1:
        type1 = response['types'][0]['type']['name']
        type2 = 'none'
    else:
        type1 = response['types'][0]['type']['name']
        type2 = response['types'][1]['type']['name']


    new_pokemon = Pokemon.objects.create(
        name = response['forms'][0]['name'],
        api_id = response['id'],
        health = 100,
        wins = 0,
        type1 = type1,
        type2 = type2,
        image = 'https://img.pokemondb.net/artwork/large/squirtle.jpg',
        url = response['forms'][0]['url'],
        owner = user,
    )

    context = {
        "user" : user,
        "collected" : Pokemon.objects.filter(owner = user),
    }

    return redirect('/account/' + str(user.id) +'/view', context)

def pokemon_modal(request, pokemon_id):
    if 'user_id' not in request.session:
        return redirect('/login_registration')

    pokemon_info = Pokemon.objects.filter(id = pokemon_id)

    context = {
        'pokemon_info' : pokemon_info,
    }
    
    return render(request, "pokemon_modal.html", context)

#Battle Temp
def battle(request, user_id):
    
    user = User.objects.get(id= user_id)

    collected = Pokemon.objects.filter(owner = user)

    request.session['battlePokemon'] = user.pokemon1


    request.session['userHealth'] = 100
    request.session['userDodge'] = 0
    request.session['userBuff'] = 1

    # Generate Enemy
    enemy_pokemon = str(random.randint(1, 889))

    request.session['enemyPokemonID'] = enemy_pokemon

    request.session['enemyHealth'] = 100
    request.session['enemyBuff'] = 1
    request.session['enemyDodge'] = 0
    request.session['lastEnemyMove'] = ''
    response = requests.get('https://pokeapi.co/api/v2/pokemon/'+ enemy_pokemon).json()
    name = response['name']
    image = str('https://img.pokemondb.net/artwork/large/' + str(name) +'.jpg')
    request.session['enemyImg'] = image
    request.session['enemyName'] = str(name)

    context = {
        'user' : user,
        'collected' : collected,
    }

    return render(request, 'battle.html', context)

#Leaderboard Temp
def leaderboard(request, user_id):
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=20').json()
    context = {'pokemon' : response['results']}
    return render(request, 'leaderboard.html', context)


# # Pokemon temp
def pokemon(request):
    if 'user_id' in request.session:
        return redirect('/home')

    randomnumber = 1-889

    response = requests.get('https://pokeapi.co/api/v2/pokemon/'+ str(randomnumber) + '.jpg' ).json()

    name = response['forms'][0]['name']

    image = str('https://img.pokemondb.net/artwork/large/' + str(name) +'.jpg')

    context = {
        'image' : image
        }
    return render(request, 'index.html', context)


def combat(request, ability):

    user = User.objects.get(id= request.session['user_id'])

    collected = Pokemon.objects.filter(owner = user)

    if ability == 'attack':
        a = random.randint(1, 10)
        if request.session['enemyDodge'] == 0:
            userDamage = a * request.session['userBuff']
            if request.session['enemyHealth'] <= (userDamage + 0):
                request.session['enemyHealth'] = 0
                request.session['lastUserMove'] = str('Attacked for ' + str(userDamage)+ '!')
                request.session['userBuff'] = 1
            else:
                request.session['enemyHealth'] = round((request.session['enemyHealth'] - userDamage), 0)
                request.session['userBuff'] = 1
                request.session['lastUserMove'] = str('Attacked for ' + str(userDamage)+ '!')
        else: 
            request.session['enemyDodge'] = 0
            request.session['userBuff'] = 1
            request.session['lastUserMove'] = str('Tried to attack but they dodged!')
        
    if ability == 'heal':
        h = random.randint(1, 10)
        if request.session['userHealth'] >= (100-h):
            request.session['userHealth'] = 100
            request.session['lastUserMove'] = str('Healed for ' + str(h) + '!')
        else:
            request.session['userHealth'] = request.session['userHealth'] + h
            request.session['lastUserMove'] = str('Healed for ' + str(h) + '!')

    if ability == 'dodge':
        request.session['userDodge'] = 1
        request.session['lastUserMove'] = 'Dodged the next attack!'
    if ability == 'buff':
        request.session['userBuff'] = request.session['userBuff'] + .5
        request.session['lastUserMove'] = 'Buffed your next attack!'

    request.session['enemyDodge'] = 0

    context = {
        'user' : user,
        'collected' : collected,
    }

    if request.session['enemyHealth'] == 0:
        return render(request, 'battle.html', context)
    else:
        return redirect('/account/' + str(user.id) + '/battle/aiCombat', context)

    

def aiCombat(request, user_id):

    user = User.objects.get(id= user_id)

    collected = Pokemon.objects.filter(owner = user)

    x = random.randint(1, 100)
    if 65 < x <= 100:
        a = random.randint(1, 10)
        if request.session['userDodge'] == 0:
            enemyDamage = a * request.session['enemyBuff']
            if request.session['userHealth'] <= enemyDamage:
                request.session['userHealth'] = 0
                request.session['enemyBuff'] = 1
                request.session['lastEnemyMove'] = str('Attacked for ' + str(enemyDamage)+ '!')
            else:
                request.session['userHealth'] = round(request.session['userHealth'] - (enemyDamage), 0)
                request.session['enemyBuff'] = 1
                request.session['lastEnemyMove'] = str('Attacked for ' + str(enemyDamage)+ '!')
        else: 
            request.session['userDodge'] = 0
            request.session['enemyBuff'] = 1
            request.session['lastEnemyMove'] = str('Tried to attack but you dodged!')
        

    if 30 < x <= 65:
        h = random.randint(1, 10)
        if request.session['enemyHealth'] >= (100-h):
            request.session['enemyHealth'] = 100
            request.session['lastEnemyMove'] = str('Healed for ' + str(h) + '!')
        else:
            request.session['enemyHealth'] = request.session['enemyHealth'] + h
            request.session['lastEnemyMove'] = str('Healed for ' + str(h)+ '!')

    if 15 < x <= 30:
        request.session['enemyDodge'] = 1
        request.session['lastEnemyMove'] = 'Will Dodge your next attack!'

    if 1 < x <= 15:
        request.session['enemyBuff'] = request.session['enemyBuff'] + .5
        request.session['lastEnemyMove'] = 'Buffed themselves!'

    request.session['userDodge'] = 0

    context = {
        'user' : user,
        'collected' : collected,
    }

    return render(request, 'battle.html', context)

def changePokemon(request,user_id, pokemon):

    user = User.objects.get(id= user_id)

    collected = Pokemon.objects.filter(owner = user)

    request.session['battlePokemon'] = pokemon

    context = {
        'user' : user,
        'collected' : collected,
    }

    return render(request, 'battle.html', context)

def changePrimary(request, slot, pokemon):

    user = User.objects.get(id= request.session['user_id'])

    collected = Pokemon.objects.filter(owner = user)

    if slot == 1:
        user.pokemon1 = pokemon

    if slot == 2:
        user.pokemon2 = pokemon

    if slot == 3:
        user.pokemon3 = pokemon

    user.save()

    context = {
        'user' : user,
        'collected' : collected,
    }

    return redirect('/account/' + str(user.id) + '/view')