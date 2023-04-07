from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import generics, permissions
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.utils import timezone
from datetime import datetime, timedelta, time

from functools import reduce


from .serializers import UserSerializer, RegisterSerializer,\
                        MealSerializer, FoodSerializer, NutrientSerializer

from .mscript import *


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            "Endpoint": "/accounts/login/",
            "method": ["POST"],
            "body": {
                "username": "",
                "password": ""
            },
            "description": "Returns an id if username and password is valid."
        },
        {
            "Endpoint": "accounts/register/",
            "method": ["POST"],
            "body": {
                "username": "",
                "password": ""
            },
            "description": "Create a new user if username and password is valid, then return user id."
        },
        {
            "Endpoint": "accounts/profile/",
            "method": ["GET"],
            "body": {
                "user_id": 0,
            },
            "description": "Return details about an user if user_id exists."
        },




        {
            "Endpoint": "/load_data/",
            "method": ["GET"],
            "body": None,
            "description": "Load nutrients and ingredients from json file to database."
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
            "description": 'Show details of the food with the corresponding id. If show_details is true, it will show the whole nutrients value of the food.'
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
            "description": 'Show details of the food with the corresponding id. If show_details is true, it will show the whole nutrients value of the food.'
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
            "description": '''Show a list of meals of the user with the user_id, filtered by the same date as the time input.'''
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
            "description": '''Show a list of meals of the user with the user_id, filtered by the same week as the time input.'''
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
                "food_set": [
                    {
                        "food_name": "",
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
    username = data['username']
    password = data['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        # login(request, user)
        return Response({
            "user_id": user.id
            })
    else:
        return HttpResponseBadRequest("Username or password is invalid.")

@api_view(['POST'])
def register_view(request):
    data = request.data
    username = data['username']
    password = data['password']
    if (not username or not password):
        return HttpResponseBadRequest("Both username and password field is required.")

    User = get_user_model()
    if User.objects.filter(username=username).count():
        return HttpResponseBadRequest("Username is already taken.")
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return Response({
        "message": "User %s registered." % username,
        "user_id": user.id
    })


@api_view(['POST'])
def logout_view(request):
    user = request.user
    if (user is None):
        return Response({"message": "No user logged in."})
    logout(request)
    return Response({"message": "Logged out."})
@api_view(['GET'])
def user_profile_view(request):
    user = User.objects.get(id = request.data['user_id'])
    if not user.is_authenticated:
        return Response("Anonymous User")
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
    


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


def get_food_render_data(food, show_details=False):
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
                nutrient_amount = ingredient_dict_element["nutrient_set"][nutrient_name]
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
                    nutrient_amount = ingredient_dict_element["nutrient_set"][nutrient_name]
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

    render_data = []
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
        render_data.append(meal_render_data)

    if (show_total):
        total_nutrient_dict["nutrient_set"] = total_nutrient_set_dict
        render_data.append({"total_nutrients_value" : total_nutrient_dict})
                


    return render_data


@api_view(['GET', 'POST'])
def getFoods(request):
    
    foods = Food.objects.all()
    data = request.data
    search_input = data.setdefault('search_input', '')

    
    foods = foods.filter(food_name__icontains=search_input)

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
    food = Food.objects.create(food_name=data['food_name'])
    ingredient_object_dict = get_ingredient_object_dict_by_name()
    for ingr in data['ingredient_set']:
        ii = IngredientInstance.objects.create(
            ingredient=ingredient_object_dict[ingr["ingredient_name"]], 
            food=food,
            amount=ingr["amount"]
        )
    get_food_dict_by_id(True)
    return Response({"message": "Food created."})

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
    render_data = get_meals_render_data(list(meals), show_details=show_details, show_total=show_total)

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
    date = data.setdefault('date', timezone.now())
    today = date.date()
    tomorrow = today + timedelta(days=1)
    time_start = datetime.combine(today, time())
    time_end = datetime.combine(tomorrow, time())
    meals = Meal.objects.filter(user=user, time__gte=time_start, time__lte=time_end, title__contains=search_input)
    render_data = get_meals_render_data(list(meals), show_details=show_details, show_total=show_total)

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
    date = data.setdefault('date', timezone.now())
    time_start = datetime.combine(date.date() - timedelta(days=date.weekday()), time())
    time_end = datetime.combine(time_start + timedelta(days=7), time())
    meals = Meal.objects.filter(user=user, time__gte=time_start, time__lte=time_end, title__contains=search_input)
    render_data = get_meals_render_data(list(meals), show_details=show_details, show_total=show_total)

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
        user = user
    )

    food_dict = get_food_dict_by_name()
    for fidict in data["food_set"]:
        foodinstance = FoodInstance(amount = fidict["amount"], food=food_dict[fidict["food_name"]], meal=meal)
        foodinstance.save()



    return Response(get_meals_render_data([meal]))


@api_view(['PUT'])
def updateMeal(request, pk):

    meal = Meal.objects.get(id=pk)

    data = request.data

    meal.title = data['title']
    meal.time = data['time']

    meal.foodinstance_set.all().delete()
    food_dict = get_food_dict_by_name()
    for fidict in data["food_set"]:
        foodinstance = FoodInstance(amount = fidict["amount"], food=food_dict[fidict["food_name"]], meal=meal)
        foodinstance.save()
    
    
    return Response(get_meals_render_data([meal]))

@api_view(['DELETE'])
def deleteMeal(request, pk):
    if not Meal.objects.filter(id=pk).exists():
        return HttpResponseBadRequest("Meal is not exist.")
    meal = Meal.objects.get(id=pk)
    meal.delete()

    return Response( { 'message' : "Meal was deleted."} )