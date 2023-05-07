from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest


from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from rest_framework.decorators import api_view
from rest_framework import generics, permissions
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from datetime import datetime, timedelta, time

from django.db.models import Q
from functools import reduce
import operator


from .serializers import UserSerializer,\
                        MealSerializer, FoodSerializer, NutrientSerializer


from django.db.models.fields.files import ImageFieldFile
from .mscript import *
import base64
import os
import re
from django.utils import timezone


User = get_user_model()


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            "Endpoint": "/accounts/login/",
            "method": ["POST"],
            "body": {
                "email": "",
                "password": ""
            },
            "description": "Returns an id if email and password is valid."
        },
        {
            "Endpoint": "accounts/register/",
            "method": ["POST"],
            "body": {
                "email": "",
                "password": "",
                "first_name": "",
                "last_name": "",
            },
            "description": "Create a new user if email and password is valid, then return user id."
        },
        {
            "Endpoint": "accounts/profile/",
            "method": ["POST"],
            "body": {
                "user_id": 0,
            },
            "description": "Return details about an user if user_id exists."
        },
        {
            "Endpoint": "accounts/profile/id/upload_profile_image/",
            "method": ["POST"],
            "body": {
                "file":
                {
                    "filename": "",
                    "content": "bytes",
                }
            },
            "description": 'Upload image for user with the corresponding id.'
        },
        {
            "Endpoint": "accounts/id/add_customer",
            "method": ["POST"],
            "body": {
                "customer_id": 1
            },
            "description": 'Add customer for user with the corresponding id.'
        },
        {
            "Endpoint": "accounts/id/add_specialist",
            "method": ["POST"],
            "body": {
                "specialist_id": 1
            },
            "description": 'Add specialist for user with the corresponding id.'
        },
        {
            "Endpoint": "/get_specialists/",
            "method": ["GET"],
            "body": None,
            "description": "Get all specialists."
        },
        {
            "Endpoint": "/load_data/",
            "method": ["GET"],
            "body": None,
            "description": "Load nutrients and ingredients from json file to database."
        },
        {
            "Endpoint": "/load_sample_foods_data/",
            "method": ["GET"],
            "body": None,
            "description": "Load 5 example foods to database."
        },


        {
            "Endpoint": "/nutrients/",
            "method": ["GET", "POST"],
            "body": {
                "search_input": "abc",
            },
            "description": "Show a list of nutrients available."
        },
        {
            "Endpoint": "/nutrients/id/",
            "method": ["GET"],
            "body": None,
            "description": '''Show details of the nutrient with the corresponding id. Example: /nutrients/1/.'''
        },


        {
            "Endpoint": "/ingredients/",
            "method": ["GET", "POST"],
            "body": {
                "show_details": False,
                "search_input": "abc",
                "page" : 1,
                "page_size": 10,
            },
            "description": '''Show a list of ingredients. If show_details is true, it will show the whole nutrients value of the ingredient.'''
        },
        {
            "Endpoint": "/ingredients/id/",
            "method": ["GET", "POST"],
            "body": {
                "show_details": False,
            },
            "description": '''Show details of the ingredient with the corresponding id. Example: /ingredients/1/. If show_details is true, it will show the whole nutrients value of the ingredient.'''
        },


        {
            "Endpoint": "/foods/",
            "method": ["GET", "POST"],
            "body": {
                "user_id": 1,
                "show_details": False,
                "show_total": False,
                "search_input": "abc",
                "page" : 1,
                "page_size": 10,
            },
            "description": 'Show a list of foods. If show_details is true, it will show the whole nutrients value of the foods.'
        },
        {
            "Endpoint": "/foods/id/",
            "method": ["GET", "POST"],
            "body": {
                "show_details": False,
                "show_total": False,
            },
            "description": 'Show details of the food with the corresponding id. If show_details is true, it will show the whole nutrients value of the food.'
        },
        {
            "Endpoint": "/foods/create/",
            "method": ["POST"],
            "body": {
                "food_name": "",
                "user_id": 1,
                "ingredient_set": [
                    {
                        "ingredient_name": "",
                        "amount": 0,
                    }
                ]
            },
            "description": 'Create a food.'
        },
        {
            "Endpoint": "/foods/id/update/",
            "method": ["PUT"],
            "body": {
                "food_name": "",
                "ingredient_set": [
                    {
                        "ingredient_name": "",
                        "amount": 0,
                    }
                ]
            },
            "description": 'Update details of the food with the corresponding id.'
        },
        {
            "Endpoint": "/foods/id/upload_image/",
            "method": ["POST"],
            "body": {
                "file":
                {
                    "filename": "",
                    "content": "bytes",
                }
            },
            "description": 'Upload image for the food with the corresponding id.'
        },
        {
            "Endpoint": "/foods/id/delete/",
            "method": ["DELETE"],
            "body": {
                "food_name": "",
                "ingredient_set": [
                    {
                        "ingredient_name": "",
                        "amount": 0,
                    }
                ]
            },
            "description": 'Delete the food with the corresponding id.'
        },


        {
            "Endpoint": "/meals/",
            "method": ["GET", "POST"],
            "body": {
                "user_id" : 0,
                "search_input": "abc",
                "show_details": False,
                "show_total": False,
            },
            "description": '''Show a list of meals of the user with the user_id. If show_details is true, it will show the whole nutrients value of the meals. If show_total is true, it will calculate the total nutrients value of the meals.'''
        },
        {
            "Endpoint": "/meals/bydate/",
            "method": ["GET", "POST"],
            "body": {
                "user_id" : 0,
                "search_input": "abc",
                "show_details": False,
                "show_total": False,
                "time": "",
            },
            "description": '''Show a list of meals filtered by the same date as the time input.'''
        },
        {
            "Endpoint": "/meals/byweek/",
            "method": ["GET", "POST"],
            "body": {
                "user_id" : 0,
                "search_input": "abc",
                "show_details": False,
                "show_total": False,
                "time": "",
            },
            "description": '''Show a list of meals filtered by the same week as the time input.'''
        },
        {
            "Endpoint": "/meals/id/",
            "method": ["GET", "POST"],
            "body": {
                "show_details": False,
                "show_total": False,
            },
            "description": '''Show the details of the meal with the corresponding meal id.'''
        },
        {
            "Endpoint": "/meals/create/",
            "method": ["POST"],
            "body": {
                "user_id" : 0,
                "title": "",
                "time" : "",
                "date": "",
                "food_set": [
                    {
                        "food_id": "",
                        "amount": ""
                    }
                ]
            },
            "description": '''Create a meal for an user.'''
        },
        {
            "Endpoint": "/meals/id/update/",
            "method": ["PUT"],
            "body": {
                "title": "",
                "time" : "",
                "food_set": [
                    {
                        "food_name": "",
                        "amount": ""
                    }
                ]
            },
            "description": '''Update a meal with an id.'''
        },
        {
            "Endpoint": "/meals/id/delete/",
            "method": ["DELETE"],
            "body": None,
            "description": '''Delete a meal with the corresponding id.'''
        },

    ]
    return Response(routes)

@api_view(['POST'])
def login_view(request):
    data = request.data
    email = data['email']
    password = data['password']

    user = authenticate(request, email=email, password=password)
    if user is not None:
        # login(request, user)
        serializer = UserSerializer(user, many=False)
        response = {
            "user_id": user.id
        }
        response.update(serializer.data)
        return Response(response)
    else:
        return HttpResponseBadRequest("Email or password is invalid.")

@api_view(['POST'])
def register_view(request):
    data = request.data
    email = data['email']
    password = data['password']
    first_name = data.setdefault('first_name', '')
    last_name = data.setdefault('last_name', '')
    role = data.setdefault('role', 'Normal')
    if (not email or not password):
        return HttpResponseBadRequest("Both email and password field is required.")

    role_choices = []
    for role_choice in User.Role.choices:
        role_choices.append(role_choice[0])
    if (role not in role_choices):
        role = User.Role.NORMAL
    if User.objects.filter(email=email).count():
        return HttpResponseBadRequest("This email has already been registered before.")
    user = User.objects.create_user(email=email, password=password, role=role, first_name=first_name, last_name=last_name)
    user.save()
    serializer = UserSerializer(user, many=False)
    response = {
        "message": "User %s registered." % user,
        "user_id": user.id
    }
    response.update(serializer.data)
    return Response(response)


@api_view(['POST'])
def user_profile_view(request):
    user = User.objects.get(id = request.data['user_id'])
    if not user.is_authenticated:
        return Response({"message": "Anonymous User"})
    return Response(serialize_user(user))

@api_view(["GET", "POST"])
def get_users(request):
    data = request.data
    search_input = data.setdefault('search_input', '')
    users = User.objects.filter(reduce(operator.or_, (Q(first_name__icontains=x) | Q(last_name__icontains=x) for x in search_input.strip().split(' '))))
    return Response(serialize_users(users))


@api_view(["GET"])
def get_specialists(request):
    specialists = User.objects.filter(role="Specialist")
    return Response(serialize_users(specialists))


@api_view(["POST"])
def uploadProfileImage(request, pk):

    data = request.data
    filename_with_extension = data['file']['filename']
    (filename, extension) = os.path.splitext(filename_with_extension)

    image_content = data['file']['content']
    decoded_content = base64.b64decode(image_content)
    newfilename = "images/profile_image/" \
        + filename + re.sub(r'[+:. ]', '-', str(timezone.now())) + extension

    os.makedirs(os.path.dirname("media/" + newfilename), exist_ok=True)
    with open("media/" + newfilename, 'wb') as f:
        f.write(decoded_content)

    user = User.objects.get(id=pk)
    user.profile_image.name = newfilename
    user.save()
    return Response({"message":"Uploaded image for %s." % user})


@api_view(['POST'])
def add_specialist(request, pk):
    data = request.data

    user = User.objects.get(id=pk)
    user.specialist_id = data["specialist_id"]
    user.save()
    return Response({"message": "Added specialist for %s." % user})


@api_view(['POST'])
def add_customer(request, pk):
    data = request.data

    user = User.objects.get(id=pk)
    user.customer_id = data["customer_id"]
    user.save()
    return Response({"message": "Added customer for %s." % user})


@api_view(['GET'])
def loadNutrientsData(request):
    load_nutrients_from_file()

    nutrients = Nutrient.objects.all()
    serializer = NutrientSerializer(nutrients, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def loadIngredientsData(request):
    load_ingredients_from_file()

    ingredients = Ingredient().objects.all()
    serializer = IngredientSerializer(ingredients, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def loadSampleFoodsData(request):
    load_nutrients_from_file()
    load_ingredients_from_file()
    sample_data = \
    [
        {
            "food_name": "Egg fried rice",
            "ingredient_set": [
                {
                    "ingredient_name": "Egg",
                    "amount": 240.0,
                },
                {
                    "ingredient_name": "Olive oil",
                    "amount": 65.0,
                },
                {
                    "ingredient_name": "Onion",
                    "amount": 50.0,
                },
                {
                    "ingredient_name": "Rice brown",
                    "amount": 250.0,
                }
            ]
        },
        {
            "food_name": "Omelet",
            "ingredient_set": [
                {
                    "ingredient_name": "Butter",
                    "amount": 50.0,
                },
                {
                    "ingredient_name": "Egg",
                    "amount": 180.0,
                }
            ]
        },
        {
            "food_name": "Air Fryer Beef & Broccoli",
            "ingredient_set": [
                {
                    "ingredient_name": "Beef",
                    "amount": 453.0,
                },
                {
                    "ingredient_name": "Broccoli",
                    "amount": 340.0,
                },
                {
                    "ingredient_name": "Garlic",
                    "amount": 16.0,
                },
                {
                    "ingredient_name": "Ginger",
                    "amount": 12.0,
                },
                {
                    "ingredient_name": "Wine red",
                    "amount": 11.8,
                }
            ]
        },
        {
            "food_name": "Beef Wellington",
            "ingredient_set": [
                {
                    "ingredient_name": "Beef",
                    "amount": 907.2,
                },
                {
                    "ingredient_name": "Butter",
                    "amount": 17.0,
                },
                {
                    "ingredient_name": "Egg",
                    "amount": 80.0,
                },
                {
                    "ingredient_name": "Pepper",
                    "amount": 20.0,
                }
            ]
        },
        {
            "food_name": "Grandma's Apple Pie",
            "ingredient_set": [
                {
                    "ingredient_name": "Apples",
                    "amount": 400.0,
                },
                {
                    "ingredient_name": "Butter",
                    "amount": 64.72,
                }
            ]
        }
    ]
    if (not User.objects.filter(id=2).exists()):
        return HttpResponseBadRequest("Invalid user_id.")
    user = User.objects.get(id=2)
    ingredient_dict = get_ingredient_object_dict_by_name()
    for fdata in sample_data:
        if (Food.objects.filter(food_name=fdata['food_name']).exists()):
            continue
        food = Food.objects.create(
            food_name=fdata['food_name'],
            user=user
        )
        for isdata in fdata['ingredient_set']:
            ii = IngredientInstance.objects.create(
                amount=isdata['amount'],
                ingredient=ingredient_dict[isdata['ingredient_name']],
                food=food,
                )
    return Response({"message": "Loaded."})

@api_view(['GET'])
def loadData(request):
    load_nutrients_from_file()
    load_ingredients_from_file()

    return Response({"message" : "Loaded nutrients and ingredients data."})




@api_view(['GET', 'POST'])
def getNutrients(request):
    nutrients = Nutrient.objects.all()

    data = request.data
    search_input = data.setdefault('search_input', '')
    nutrients = nutrients.filter(nutrient_name__icontains=search_input)
    serializer = NutrientSerializer(nutrients, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getNutrient(request, pk):
    nutrient = Nutrient.objects.get(id=pk)
    serializer = NutrientSerializer(nutrient)
    return Response(serializer.data)




def serialize_ingredient(ingredient : Ingredient):
    ret = {
        "id": ingredient.id,
        "ingredient_name": ingredient.ingredient_name,
        "fat": ingredient.fat,
        "calories": ingredient.calories,
        "proteins": ingredient.proteins,
        "carbohydrates": ingredient.carbohydrates,
        "serving": ingredient.serving,
    }
    return ret

def serialize_food(food : Food):
    ret = {
        "id" : food.id,
        "food_name" : food.food_name,
    }
    if (food.image):
        ret['image'] = food.image.url
    return ret

def serialize_meal(meal : Meal):
    ret = {
        "id" : meal.id,
        "title" : meal.title,
        "time" : meal.time,
        "user_id": meal.user.id
    }
    return ret





def get_ingredient_render_data(ingredient, show_details=False):
    if (not show_details):
        return serialize_ingredient(ingredient)

    ingredient_dict = get_ingredient_dict_by_id()
    render_data = ingredient_dict[ingredient.id]

    return render_data
def get_ingredients_render_data(ingredients, show_details=False):
    render_data = []
    ingredient_dict = get_ingredient_dict_by_id()
    for ingredient in ingredients:
        if (not show_details):
            render_data.append(serialize_ingredient(ingredient))
        else:
            render_data.append(ingredient_dict[ingredient.id])
    return render_data

# def get_ingredient_dict_by_id():
#     global ingredient_dict_by_id
#     if (not ingredient_dict_by_id):
#         ingredients_render_data = get_ingredients_render_data(list(Ingredient.objects.all()), show_details=True)
#         for ii in ingredients_render_data:
#             ingredient_dict_by_id[ii["id"]] = ii

#     return ingredient_dict_by_id


def get_food_render_data(food, show_details=False, show_total=False):
    render_data = serialize_food(food)
    render_data["ingredient_set"] = []
    ingredient_dict = get_ingredient_dict_by_id()
    for ingr in food.ingredientinstance_set.values_list():
        iiid = ingr[1]
        iiamount = ingr[2]
        ingredient_dict_element = ingredient_dict[iiid]
        iidict = {}
        ingredient_name = ingredient_dict_element["ingredient_name"]
        iidict["ingredient_name"] = ingredient_name
        iidict["amount"] = iiamount
        for macronutrients in ["fat", "calories", "proteins", "carbohydrates"]:
            iidict[macronutrients] = float(ingredient_dict_element[macronutrients]) * float(iiamount) / 100
        iidict["nutrient_set"] = {}
        if (show_details):
            for nutrient_name in ingredient_dict_element["nutrient_set"]:
                nutrient_amount = ingredient_dict_element["nutrient_set"][nutrient_name]["ammount"]
                iidict["nutrient_set"][nutrient_name] = float(nutrient_amount) * float(iiamount) / 100
        render_data["ingredient_set"].append(iidict)
    return render_data


def get_foods_render_data(foods, show_details=False, show_total=False):
    render_data = []
    nutrient_dict = get_nutrient_dict_by_name()
    ingredient_dict = get_ingredient_dict_by_id()
    total_nutrient_dict = {}
    total_nutrient_set_dict = {}
    rda_dict = {}
    for nutrient_name in nutrient_dict:
        total_nutrient_set_dict[nutrient_name] = {"amount": 0, "percentage": 0}
        rda_dict[nutrient_name] = nutrient_dict[nutrient_name].rda
    for macronutrients in ["fat", "calories", "proteins", "carbohydrates"]:
        total_nutrient_dict[macronutrients] = 0
    for food in foods:

        food_render_data = serialize_food(food)
        food_render_data["ingredient_set"] = []
        for ingr in food.ingredientinstance_set.values_list():
            iiid = ingr[1]
            iiamount = ingr[2]
            ingredient_dict_element = ingredient_dict[iiid]
            iidict = {}
            ingredient_name = ingredient_dict_element["ingredient_name"]
            iidict["ingredient_name"] = ingredient_name
            iidict["amount"] = iiamount
            for macronutrients in ["fat", "calories", "proteins", "carbohydrates"]:
                iidict[macronutrients] = float(ingredient_dict_element[macronutrients]) * float(iiamount) / 100
            iidict["nutrient_set"] = {}
            if (show_details or show_total):
                for nutrient_name in ingredient_dict_element["nutrient_set"]:
                    nutrient_amount = ingredient_dict_element["nutrient_set"][nutrient_name]["ammount"]
                    iidict["nutrient_set"][nutrient_name] = float(nutrient_amount) * float(iiamount) / 100
            food_render_data["ingredient_set"].append(iidict)
        render_data.append(food_render_data)

        if (show_total):
            food_ingredient_set = food_render_data['ingredient_set']
            for ingr in food_ingredient_set:
                for macronutrients in ["fat", "calories", "proteins", "carbohydrates"]:
                    total_nutrient_dict[macronutrients] += float(ingr[macronutrients])
                ingr_nutrient_set = ingr['nutrient_set']
                for nutrient_name in ingr_nutrient_set:
                    total_nutrient_set_dict[nutrient_name]['amount'] += float(ingr_nutrient_set[nutrient_name])
                    total_nutrient_set_dict[nutrient_name]['percentage'] += float(ingr_nutrient_set[nutrient_name]) / float(rda_dict[nutrient_name]) * 10000

    if (show_total):
        total_nutrient_dict["nutrient_set"] = total_nutrient_set_dict
        render_data.append({"total_nutrients_value" : total_nutrient_dict})

    return render_data

def get_meals_render_data(meals, show_details=False, show_total=False):

    render_data = {
        "meals": [],
        "total_nutrients_value": None
    }
    nutrient_dict = get_nutrient_dict_by_name()
    ingredient_dict = get_ingredient_dict_by_id()
    food_dict = get_food_dict_by_id()
    total_nutrient_dict = {}
    total_nutrient_set_dict = {}
    rda_dict = {}
    for nutrient_name in nutrient_dict:
        total_nutrient_set_dict[nutrient_name] = {"amount": 0, "percentage": 0}
        rda_dict[nutrient_name] = nutrient_dict[nutrient_name].rda
    for macronutrients in ["fat", "calories", "proteins", "carbohydrates"]:
        total_nutrient_dict[macronutrients] = 0

    for meal in meals:
        meal_render_data = serialize_meal(meal)
        meal_render_data['food_set'] = []
        for fi in meal.foodinstance_set.values_list():
            food_id = fi[1]
            food_object = food_dict[food_id]
            food_amount = fi[2]
            food_render_data = get_food_render_data(food_object, show_details=show_details or show_total)
            food_render_data['amount'] = food_amount
            food_ingredient_set_dict = food_render_data['ingredient_set']
            new_food_ingredient_set_dict = []
            for ingredient_dict in food_ingredient_set_dict:
                ingredient_dict['amount'] = float(ingredient_dict['amount']) * float(food_amount) / 100
                for macronutrients in ["fat", "calories", "proteins", "carbohydrates"]:
                    ingredient_dict[macronutrients] = float(ingredient_dict[macronutrients]) * float(food_amount) / 100
                    if (show_total):
                        total_nutrient_dict[macronutrients] += ingredient_dict[macronutrients]
                ingredient_nutrient_set_dict = ingredient_dict['nutrient_set']
                for nutrient_name in ingredient_nutrient_set_dict:
                    ingredient_nutrient_set_dict[nutrient_name] = float(ingredient_nutrient_set_dict[nutrient_name]) * float(food_amount) / 100
                    if (show_total):
                        total_nutrient_set_dict[nutrient_name]['amount'] += float(ingredient_nutrient_set_dict[nutrient_name])
                        total_nutrient_set_dict[nutrient_name]['percentage'] += float(ingredient_nutrient_set_dict[nutrient_name]) / float(rda_dict[nutrient_name]) * 10000
                ingredient_dict['nutrient_set'] = ingredient_nutrient_set_dict
                new_food_ingredient_set_dict.append(ingredient_dict)
            food_render_data['ingredient_set'] = new_food_ingredient_set_dict
            meal_render_data['food_set'].append(food_render_data)
        render_data["meals"].append(meal_render_data)

    if (show_total):
        total_nutrient_dict["nutrient_set"] = total_nutrient_set_dict
        render_data["total_nutrients_value"] = total_nutrient_dict



    return render_data


@api_view(['GET', 'POST'])
def getFoods(request):

    foods = Food.objects.all()
    data = request.data
    search_input = data.setdefault('search_input', '')

    user_id = data.setdefault('user_id', -1)
    if not User.objects.filter(id=user_id).exists():
        foods = foods.filter(food_name__icontains=search_input)
    else:
        user = User.objects.get(id = user_id)
        foods = foods.filter(food_name__icontains=search_input, user=user)

    show_details = data.setdefault('show_details', False)
    show_total = data.setdefault('show_total', False)
    page = data.setdefault('page', 1)
    pagesize = data.setdefault('pagesize', 10)
    page -= 1
    list_to_show = list(foods)[page * pagesize: (page + 1) * pagesize]
    return Response(get_foods_render_data(list_to_show, show_details=show_details, show_total=show_total))


@api_view(['GET', 'POST'])
def getFood(request, pk):
    food = Food.objects.get(id=pk)

    data = request.data
    show_details = data.setdefault('show_details', True)
    show_total = data.setdefault('show_total', False)
    return Response(get_foods_render_data([food], show_details=show_details, show_total=show_total))

@api_view(['POST'])
def createFood(request):
    data = request.data

    user_id = data.setdefault('user_id', -1)
    if (not User.objects.filter(id=user_id).exists()):
        return HttpResponseBadRequest("Invalid user_id.")
    user = User.objects.get(id = user_id)

    food = Food.objects.create(
        food_name=data['food_name'],
        food_description=data['food_description'],
        user=user
    )
    ingredient_object_dict = get_ingredient_object_dict_by_name()
    for ingr in data['ingredient_set']:
        ii = IngredientInstance.objects.create(
            ingredient=ingredient_object_dict[ingr["ingredient_name"]],
            food=food,
            amount=ingr["amount"]
        )
    get_food_dict_by_id(True)
    return Response({
        "message": "Food created.",
        "data": {
            "id": food.id
        }
    })



@api_view(['PUT'])
def updateFood(request, pk):
    data = request.data

    food = Food.objects.get(id=pk)
    food.food_name = data['food_name']
    food.save()
    food.ingredientinstance_set.all().delete()
    ingredient_object_dict = get_ingredient_object_dict_by_name()
    for ingr in data['ingredient_set']:
        ii = IngredientInstance.objects.create(
            ingredient=ingredient_object_dict[ingr["ingredient_name"]],
            food=food,
            amount=ingr["amount"]
        )

    get_food_dict_by_id(True)
    return Response({"message": "Food updated."})


@api_view(['POST'])
def uploadFoodImage(request, pk):
    data = request.data
    filename_with_extension = data['file']['filename']
    (filename, extension) = os.path.splitext(filename_with_extension)

    image_content = data['file']['content']
    decoded_content = base64.b64decode(image_content)
    newfilename = "images/food/" \
        + filename + re.sub(r'[+:. ]', '-', str(timezone.now())) + extension

    os.makedirs(os.path.dirname("media/" + newfilename), exist_ok=True)
    with open("media/" + newfilename, 'wb') as f:
        f.write(decoded_content)

    food = Food.objects.get(id=pk)
    food.image.name = newfilename
    food.save()
    return Response({"message":"Uploaded image for %s." % food.food_name})


@api_view(['DELETE'])
def deleteFood(request, pk):
    Food.objects.get(id=pk).delete()
    get_food_dict_by_id(True)

    return Response({"message": "Food deleted."})

@api_view(['GET', 'POST'])
def getIngredients(request):
    ingredients = Ingredient.objects.all()

    data = request.data
    show_details = data.setdefault('show_details', False)
    search_input = data.setdefault('search_input', '')
    ingredients = ingredients.filter(ingredient_name__icontains=search_input)
    page = data.setdefault('page', 1)
    pagesize = data.setdefault('pagesize', 10)
    page -= 1
    list_to_show = list(ingredients)[page * pagesize: (page + 1) * pagesize]
    return Response(get_ingredients_render_data(list_to_show, show_details=show_details))


@api_view(['GET', 'POST'])
def getIngredient(request, pk):
    ingredient = Ingredient.objects.get(id=pk)

    data = request.data
    show_details = data.setdefault('show_details', True)
    return Response(get_ingredients_render_data([ingredient], show_details=show_details))



@api_view(['GET', 'POST'])
def getMeals(request):
    data = request.data
    user_id = data.setdefault('user_id', -1)
    if (not User.objects.filter(id=user_id).exists()):
        return HttpResponseBadRequest("Invalid user_id.")
    user = User.objects.get(id = user_id)

    data = request.data
    show_details = data.setdefault('show_details', False)
    show_total = data.setdefault('show_total', False)
    search_input = data.setdefault('search_input', '')
    meals = Meal.objects.filter(user=user, title__contains=search_input)

    page = data.setdefault('page', 1)
    pagesize = data.setdefault('pagesize', 10)
    page -= 1
    list_to_show = list(meals)[page * pagesize: (page + 1) * pagesize]
    render_data = get_meals_render_data(list_to_show, show_details=show_details, show_total=show_total)

    return Response(render_data)


@api_view(['GET', 'POST'])
def getMealsByDate(request):
    data = request.data
    user_id = data.setdefault('user_id', -1)
    if (not User.objects.filter(id=user_id).exists()):
        return HttpResponseBadRequest("Invalid user_id.")
    user = User.objects.get(id = user_id)

    data = request.data
    show_details = data.setdefault('show_details', False)
    show_total = data.setdefault('show_total', False)
    search_input = data.setdefault('search_input', '')
    date_start = datetime.strptime(data['date'], '%d-%m-%Y').date()
    date_end = date_start
    meals = Meal.objects.filter(user=user, date__gte=date_start, date__lte=date_end, title__contains=search_input)

    page = data.setdefault('page', 1)
    pagesize = data.setdefault('pagesize', 10)
    page -= 1
    list_to_show = list(meals)[page * pagesize: (page + 1) * pagesize]
    render_data = get_meals_render_data(list_to_show, show_details=show_details, show_total=show_total)

    return Response(render_data)


@api_view(['GET', 'POST'])
def getMealsByWeek(request):
    data = request.data
    user_id = data.setdefault('user_id', -1)
    if (not User.objects.filter(id=user_id).exists()):
        return HttpResponseBadRequest("Invalid user_id.")
    user = User.objects.get(id = user_id)

    data = request.data
    show_details = data.setdefault('show_details', False)
    show_total = data.setdefault('show_total', False)
    search_input = data.setdefault('search_input', '')
    date_start = datetime.strptime(data['date'], '%d-%m-%Y').date()
    date_end = (datetime.strptime(data['date'], '%d-%m-%Y') + timedelta(days=6)).date()
    meals = Meal.objects.filter(user=user, date__gte=date_start, date__lte=date_end, title__contains=search_input)

    page = data.setdefault('page', 1)
    pagesize = data.setdefault('pagesize', 10)
    page -= 1
    list_to_show = list(meals)[page * pagesize: (page + 1) * pagesize]
    render_data = get_meals_render_data(list_to_show, show_details=show_details, show_total=show_total)

    return Response(render_data)


@api_view(['GET', 'POST'])
def getMeal(request, pk):
    data = request.data


    meal = Meal.objects.get(id=pk)
    '''
    {
        "title": "BigBroccoli",
        "time" : "2023-03-27 07:00",
        "food_set": [
            {
                "food_name": "Broccoli",
                "amount": "1000"
            }
        ]
    }
    '''
    data = request.data
    show_details = data.setdefault('show_details', True)
    show_total = data.setdefault('show_total', True)
    return Response(get_meals_render_data([meal], show_details=show_details, show_total=show_total))


@api_view(['POST'])
def createMeal(request):
    data = request.data
    user_id = data.setdefault('user_id', -1)
    if (not User.objects.filter(id=user_id).exists()):
        return HttpResponseBadRequest("Invalid user_id.")
    user = User.objects.get(id = user_id)

    data = request.data
    meal = Meal.objects.create(
        title = data['title'],
        time = data['time'],
        date = datetime.strptime(data['date'], '%d-%m-%Y').date(),
        user = user
    )

    food_dict = get_food_dict_by_id()
    for fidict in data["food_set"]:
        foodinstance = FoodInstance(amount = fidict["amount"], food=food_dict[fidict["food_id"]], meal=meal)
        foodinstance.save()



    return Response(get_meals_render_data([meal]))


@api_view(['PUT'])
def updateMeal(request, pk):

    meal = Meal.objects.get(id=pk)

    data = request.data

    meal.title = data['title']
    meal.time = data['time']
    meal.date = datetime.strptime(data['date'], '%d-%m-%Y').date(),

    meal.foodinstance_set.all().delete()
    food_dict = get_food_dict_by_id()
    for fidict in data["food_set"]:
        foodinstance = FoodInstance(amount = fidict["amount"], food=food_dict[fidict["food_id"]], meal=meal)
        foodinstance.save()


    return Response(get_meals_render_data([meal]))

@api_view(['DELETE'])
def deleteMeal(request, pk):
    if not Meal.objects.filter(id=pk).exists():
        return HttpResponseBadRequest("Meal is not exist.")
    meal = Meal.objects.get(id=pk)
    meal.delete()

    return Response( { 'message' : "Meal was deleted."} )