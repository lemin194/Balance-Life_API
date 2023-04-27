from .models import Food, FoodInstance, Meal, Ingredient, IngredientInstance, Nutrient, NutrientInstance
import json

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)



def serialize_user(user : User):
    ret = {
        'id': user.id,
        'profile_image': user.profile_image.url,
        'last_login': user.last_login,
        'username' : user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'date_joined': user.date_joined,
        'role': user.role,
    }
    return ret

def serialize_users(users):
    ret = []
    for user in users:
        ret.append(serialize_user(user))
    return ret



nutrient_dict_by_id = {}
nutrient_dict_by_name = {}
ingredient_dict_by_id = {}
ingredient_object_dict_by_name = {}
food_dict_by_id = {}
food_dict_by_name = {}

def get_food_dict_by_id(update=False):
    global food_dict_by_id
    if (not food_dict_by_id or update):
        food_dict_by_id = {}
        for food in Food.objects.all():
            food_dict_by_id[food.id] = food
    return food_dict_by_id
    

def get_food_dict_by_name(update=False):
    global food_dict_by_name
    if (not food_dict_by_name or update):
        food_dict_by_name = {}
        for food in Food.objects.all():
            food_dict_by_name[food.food_name] = food
    return food_dict_by_name

def get_nutrient_dict_by_name():
    global nutrient_dict_by_name
    if (not nutrient_dict_by_name):
        nutrient_dict_by_name = {}
        for n in Nutrient.objects.all():
            nutrient_dict_by_name[n.nutrient_name] = n

    
    return nutrient_dict_by_name



def get_nutrient_dict_by_id():
    global nutrient_dict_by_id
    if (not nutrient_dict_by_id):
        nutrient_dict_by_id = {}
        for n in Nutrient.objects.all():
            nutrient_dict_by_id[n.id] = n
    return nutrient_dict_by_id


def get_ingredient_dict_by_id():
    global ingredient_dict_by_id
    if (not ingredient_dict_by_id):
        ingredient_dict_by_id = {}
        for ingredient in Ingredient.objects.all():
            ingredient_dict_element = {
                "id": ingredient.id,
                "ingredient_name": ingredient.ingredient_name,
                "fat": ingredient.fat,
                "calories": ingredient.calories,
                "proteins": ingredient.proteins,
                "carbohydrates": ingredient.carbohydrates,
                "serving": ingredient.serving,
            }
            ingredient_dict_element["nutrient_set"] = {}
            nutrient_dict = get_nutrient_dict_by_id()
            for n in ingredient.nutrientinstance_set.values_list():
                nutrient_name = nutrient_dict[n[2]].nutrient_name
                ingredient_dict_element["nutrient_set"][nutrient_name] = n[1] #amount
            ingredient_dict_by_id[ingredient.id] = ingredient_dict_element

    return ingredient_dict_by_id

def get_ingredient_object_dict_by_name():
    global ingredient_object_dict_by_name
    if (not ingredient_object_dict_by_name):
        for ingredient in Ingredient.objects.all():
            ingredient_object_dict_by_name[ingredient.ingredient_name] = ingredient
    return ingredient_object_dict_by_name

def load_nutrients_from_file(path=''):
    if (path == ''):
        path = 'data/nutrients.json'
    f = open(path)
    data = json.load(f)
    nutrient_name_set = set()
    for n in Nutrient.objects.all():
        nutrient_name_set.add(n.nutrient_name)
    for d in data:
        if (not d['name'] in nutrient_name_set):
            n = Nutrient(
                nutrient_name=d['name'],
                rda =d['rda'],
                wiki=d['wiki'],
                required=d['required'],
                category=d['type'],
            )
            n.save()


def load_ingredients_from_file(path=''):
    if (path == ''):
        path = 'data/foods.json'

    mfile = open(path)
    data = json.load(mfile)
    ingredient_name_set = set()
    for ingr in Ingredient.objects.all():
        ingredient_name_set.add(ingr.ingredient_name)
    nutrient_dict = get_nutrient_dict_by_name()
    for d in data:
        if (not d['name'] in ingredient_name_set):
            ingr = Ingredient()
            ingr.ingredient_name = d['name']
            ingr.fat = d['fat']
            ingr.calories = d['calories']
            ingr.proteins = d['proteins']
            ingr.carbohydrates = d['carbohydrates']
            ingr.serving = d['serving']
            ingr.save()
            for name in d['nutrients']:
                try:
                    nInstance = NutrientInstance()
                    nInstance.nutrient = nutrient_dict[name]
                    nInstance.ingredient = ingr
                    if (d['nutrients'][name] == None):
                        nInstance.amount = 0
                    else:
                        nInstance.amount = d['nutrients'][name]
                    nInstance.save()
                except django.db.utils.IntegrityError:
                    print(name + ' from ' + d['name'], "has an IntegrityError!")
                    print(d['nutrients'][name])
