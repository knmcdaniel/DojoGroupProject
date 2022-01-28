from django.db import models
import bcrypt, re

# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}

        duplicate_username = User.objects.filter(username=postData['username'])
        if duplicate_username:
            errors['unique'] = "Username Taken"
        else:
            username = postData['username']
            if len(username) < 2:
                errors['username_not_valid'] = "Invalid Username."

        password = postData['password']
        if len(password) < 2:
            errors['password_not_valid'] = "Invalid Password Length."

        confirm_password = postData['confirm_password']
        if password != confirm_password:
            errors['non_matching_passwords'] = "Your Passwords do not match"

        if len(errors) < 0:
            errors['create'] = ("User Created!")
        return errors
        
    def login_validator(self, postData):
        errors = {}
        username = User.objects.filter(username=postData['username'])
        if not username:
            errors['creds'] = "Login Credentials Incorrect"
        else:
            logged_user = username[0]
            if not bcrypt.checkpw(postData['password'].encode(),logged_user.password.encode()):
                errors['creds'] = "Login Credentials Incorrect"
        login_errors = errors

        return login_errors

# Will eventually be needed
# class PokemonManager(models.Manager):


class User(models.Model):
    #Object
    #id
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wins = models.IntegerField()
    loses = models.IntegerField()
    pokemon1 = models.CharField(max_length=255)
    pokemon2 = models.CharField(max_length=255)
    pokemon3 = models.CharField(max_length=255)

    #relationships
    #One to many with pokemons ----> pokemon_collected

    #methods
    objects = UserManager()

    
class Pokemon(models.Model):
    #Object
    #id
    name = models.CharField(max_length=255)
    health = models.IntegerField()
    wins = models.IntegerField()
    type1 = models.CharField(max_length=255)
    type2 = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    
    #relationships
    owner = models.ForeignKey(User, related_name="pokemon_collected", on_delete = models.CASCADE)

    #methods
    # objects = PokemonManager()

