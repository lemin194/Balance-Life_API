from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework import generics, permissions
from rest_framework.response import Response

from django.utils import timezone
from datetime import datetime, timedelta, time


from .serializers import UserSerializer, RegisterSerializer,\
                        MealSerializer, FoodSerializer, NutrientSerializer

from .mscript import *


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            "Endpoint": "/accounts/login/",
            "method": "POST",
            "body": {
                "username": "",
                "password": ""
            }
        },
        {
            "Endpoint": "accounts/register/",
            "method": "POST",
            "body": {
                "username": "",
                "password": ""
            }
        },
        {
            "Endpoint": "accounts/profile/",
            "method": "GET",
            "body": {
                "username": "",
                "password": ""
            }
        },




        {
            "Endpoint": "/load_data/",
            "method": "GET",
            "body": None,
        },
        {
            "Endpoint": "/load_food_data/",
            "method": "GET",
            "body": None,
        },
        {
            "Endpoint": "/load_nutrients_data/",
            "method": "GET",
            "body": None,
        },


        {
            "Endpoint": "/nutrients/",
            "method": "GET",
            "body": None,
        },
        {
            "Endpoint": "/nutrients/id/",
            "method": "GET",
            "body": None,
        },

        
        {
            "Endpoint": "/foods/",
            "method": "GET",
            "body": None,
        },
        {
            "Endpoint": "/foods/id/",
            "method": "GET",
            "body": None,
        },
        
        
        {
            "Endpoint": "/meals/",
            "method": "GET",
            "body": {
                "show_details": False,
                "show_total": False,
            },
        },
        {
            "Endpoint": "/meals/bydate/",
            "method": "GET",
            "body": {
                "show_details": False,
                "show_total": False,
                "time": "",
            },
        },
        {
            "Endpoint": "/meals/byweek/",
            "method": "GET",
            "body": {
                "show_details": False,
                "show_total": False,
                "time": "",
            },
        },
        {
            "Endpoint": "/meals/id/",
            "method": "GET",
            "body": {
                "show_details": False,
                "show_total": False,
            },
        },
        {
            "Endpoint": "/meals/create/",
            "method": "POST",
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
        },
        {
            "Endpoint": "/meals/id/update/",
            "method": "PUT",
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
        },
        {
            "Endpoint": "/meals/id/delete/",
            "method": "DELETE",
            "body": None,
        },

    ]
    return Response(routes)

# @api_view(['POST'])
# def login_view(request):
#     data = request.data
#     username = data['username']
#     password = data['password']

#     user = authenticate(request, username=username, password=password)
#     if user != None:
#         login(request, user)
#         return Response({"message": "User logged in."})
#     else:
#         return Response({"message":"Log in failed."})

@api_view(['POST'])
def register_view(request):
    data = request.data
    username = data['username']
    password = data['password']
    User = get_user_model()
    if User.objects.filter(username=username).count():
        return Response({"message:", "Username is already taken."})
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return Response({"message": "User registered."})

@api_view(['GET'])
def user_profile_view(request):
    user = request.user
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
def loadFoodsData(request):
    load_foods_from_file()

    foods = Food.objects.all()
    serializer = FoodSerializer(foods, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def loadData(request):
    load_nutrients_from_file()
    load_foods_from_file()

    return Response({"message" : "Loaded nutrients and foods data."})




@api_view(['GET'])
def getNutrients(request):
    nutrients = Nutrient.objects.all()
    serializer = NutrientSerializer(nutrients, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getNutrient(request, pk):
    nutrient = Nutrient.objects.get(id=pk)
    serializer = NutrientSerializer(nutrient)
    return Response(serializer.data)




def serialize_food(food : Food):
    ret = {
        "id": food.id,
        "food_name": food.food_name,
        "fat": food.fat,
        "calories": food.calories,
        "proteins": food.proteins,
        "carbohydrates": food.carbohydrates,
        "serving": food.serving,
    }
    return ret





# def get_food_render_data(food, show_details=False):
#     serializer = FoodSerializer(food)
#     render_data = serializer.data
#     if (not show_details):
#         return render_data
#     render_data['nutrient_set'] = []
#     nutrientinstance_list = list(food.nutrientinstance_set.all())
#     for ni in nutrientinstance_list:
#         nidict = {
#             "name": ni.nutrient.nutrient_name,
#             "amount": ni.amount
#         }
#         render_data['nutrient_set'].append(nidict)

#     return render_data
# def get_foods_render_data(foods, show_details=False):
#     render_data = []
#     for food in foods:
#         render_data.append(get_food_render_data(food, show_details=show_details))
#     return render_data




def get_food_render_data(food, show_details=False):
    # serializer = FoodSerializer(food)
    # render_data = serializer.data
    render_data = serialize_food(food)

    if (not show_details):
        return render_data
    render_data["nutrient_set"] = {}

    # nutrientinstance_list = list(food.nutrientinstance_set.all())
    # for ni in nutrientinstance_list:
    #     render_data['nutrient_set'][ni.nutrient.nutrient_name] = ni.amount
    for n in food.nutrientinstance_set.values_list():
        nutrient_name = Nutrient.objects.get(id=n[2]).nutrient_name
        render_data["nutrient_set"][nutrient_name] = n[1] #amount

    return render_data
def get_foods_render_data(foods, show_details=False):
    render_data = []
    for food in foods:
        render_data.append(get_food_render_data(food, show_details=show_details))
    return render_data


# def get_meals_render_data(meals, show_details=False, show_total=False):

#     render_data = []
#     total_amount = {}
#     nutrients = Nutrient.objects.all()
#     for nutrient in nutrients:
#         total_amount[nutrient.nutrient_name] = { "amount": 0, "percentage": 0 }

#     for meal in meals:
#         serializer = MealSerializer(meal)
#         meal_data = serializer.data
#         meal_data['food_set'] = []
#         foodinstance_list = list(meal.foodinstance_set.all())
#         for fi in foodinstance_list:
#             fidict = {
#                 "food_name": fi.food.food_name,
#                 "amount": fi.amount
#             }
#             if (show_details or show_total):
#                 food_data = get_food_render_data(fi.food, show_details=True)
#                 for key in ["fat", "calories", "proteins", "carbohydrates"]:
#                     food_data[key] = float(food_data[key]) * float(fi.amount) / 100
#                 for i in range(len(food_data["nutrient_set"])):
#                     nutrient_name = food_data["nutrient_set"][i]["name"]
#                     food_data["nutrient_set"][i]["amount"] = \
#                         float(food_data["nutrient_set"][i]["amount"]) * float(fi.amount) / 100
#                     food_data["nutrient_set"][i]["percentage"] = \
#                         float(food_data["nutrient_set"][i]["amount"]) / float(nutrients.get(nutrient_name=nutrient_name).rda) * 10000
                    
#                     total_amount[nutrient_name]["amount"] += food_data["nutrient_set"][i]["amount"]
#                     total_amount[nutrient_name]["percentage"] += food_data["nutrient_set"][i]["percentage"]
#                 if (show_details):
#                     fidict.update(food_data)
#             meal_data['food_set'].append(fidict)
#         render_data.append(meal_data)
#     if (show_total):
#         total_amount_response_data = []
#         for key in total_amount:
#             tadict = {"name": key, "amount": total_amount[key]["amount"], "percentage": total_amount[key]["percentage"]}
#             total_amount_response_data.append(tadict)
#         render_data.append({'total_amount': total_amount_response_data})
#     return render_data

def get_meals_render_data(meals, show_details=False, show_total=False):

    render_data = []
    total_amount = {}
    nutrients = Nutrient.objects.all()
    rda_data = {}
    if (show_details or show_total):
        for n in nutrients:
            rda_data[n.nutrient_name] = n.rda
            total_amount[n.nutrient_name] = { "amount": 0, "percentage": 0 }

    for meal in meals:
        serializer = MealSerializer(meal)
        meal_data = serializer.data
        meal_data['food_set'] = []
        foodinstance_list = meal.foodinstance_set.all()
        for fi in foodinstance_list:
            amount = fi.amount
            food_name = fi.food.food_name
            fidict = {
                "food_name": food_name,
                "amount": amount
            }
            if (show_details or show_total):
                food_data = get_food_render_data(fi.food, show_details=True)
                for macronutrients in ["fat", "calories", "proteins", "carbohydrates"]:
                    food_data[macronutrients] = float(food_data[macronutrients]) * float(amount) / 100
                for nutrient_name in food_data["nutrient_set"]:
                    food_data["nutrient_set"][nutrient_name] = \
                        float(food_data["nutrient_set"][nutrient_name]) * float(amount) / 100
                    
                    total_amount[nutrient_name]["amount"] += food_data["nutrient_set"][nutrient_name]
                    total_amount[nutrient_name]["percentage"] += float(food_data["nutrient_set"][nutrient_name]) / float(rda_data[nutrient_name]) * 10000
                if (show_details):
                    fidict.update(food_data)
            meal_data['food_set'].append(fidict)
        render_data.append(meal_data)
    if (show_total):
        total_amount_response_data = []
        for key in total_amount:
            tadict = {"name": key, "amount": total_amount[key]["amount"], "percentage": total_amount[key]["percentage"]}
            total_amount_response_data.append(tadict)
        render_data.append({'total_amount': total_amount_response_data})
    return render_data


@api_view(['GET'])
def getFoods(request):
    foods = Food.objects.all()
    
    data = request.data
    show_details = data.setdefault('show_details', False)
    return Response(get_foods_render_data(list(foods), show_details=show_details))


@api_view(['GET'])
def getFood(request, pk):
    food = Food.objects.get(id=pk)

    data = request.data
    show_details = data.setdefault('show_details', True)
    return Response(get_foods_render_data([food], show_details=show_details))



@api_view(['GET'])
def getMeals(request):
    if (not request.user.is_authenticated):
        message = {'message': 'User is not logged in.'}
        return Response(message)

    data = request.data
    show_details = data.setdefault('show_details', False)
    show_total = data.setdefault('show_total', False)
    meals = Meal.objects.filter(user=request.user)
    render_data = get_meals_render_data(list(meals), show_details=show_details, show_total=show_total)

    return Response(render_data)


@api_view(['GET'])
def getMealsByDate(request):
    if (not request.user.is_authenticated):
        message = {'message': 'User is not logged in.'}
        return Response(message)

    data = request.data
    show_details = data.setdefault('show_details', False)
    show_total = data.setdefault('show_total', False)
    date = data.setdefault('date', timezone.now())
    today = date.date()
    tomorrow = today + timedelta(days=1)
    time_start = datetime.combine(today, time())
    time_end = datetime.combine(tomorrow, time())
    meals = Meal.objects.filter(user=request.user, time__gte=time_start, time__lte=time_end)
    render_data = get_meals_render_data(list(meals), show_details=show_details, show_total=show_total)

    return Response(render_data)


@api_view(['GET'])
def getMealsByWeek(request):
    if (not request.user.is_authenticated):
        message = {'message': 'User is not logged in.'}
        return Response(message)

    data = request.data
    show_details = data.setdefault('show_details', False)
    show_total = data.setdefault('show_total', False)
    date = data.setdefault('date', timezone.now())
    time_start = datetime.combine(date.date() - timedelta(days=date.weekday()), time())
    time_end = datetime.combine(time_start + timedelta(days=7), time())
    meals = Meal.objects.filter(user=request.user, time__gte=time_start, time__lte=time_end)
    render_data = get_meals_render_data(list(meals), show_details=show_details, show_total=show_total)

    return Response(render_data)


@api_view(['GET'])
def getMeal(request, pk):
    if (not request.user.is_authenticated):
        message = {'message': 'User is not logged in.'}
        return Response(message)

    meal = Meal.objects.get(id=pk)
    if (meal.user != request.user):
        message = {'message': 'User is not authenticated for this data.'}
        return Response(message)

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
    if (not request.user.is_authenticated):
        message = {'message': 'User is not logged in.'}
        return Response(message)
    data = request.data
    meal = Meal.objects.create(
        title = data['title'], 
        time = data['time'], 
        user = request.user
    )

    create_foodinstances_from_food_set(data['food_set'], meal)

    return Response(get_meals_render_data([meal]))


@api_view(['PUT'])
def updateMeal(request, pk):
    if (not request.user.is_authenticated):
        message = {'message': 'User is not logged in.'}
        return Response(message)

    meal = Meal.objects.get(id=pk)
    if (meal.user != request.user):
        message = {'message': 'User is not authenticated for this data.'}
        return Response(message)

    data = request.data


    meal.title = data['title']
    meal.time = data['time']

    meal.foodinstance_set.all().delete()
    create_foodinstances_from_food_set(data['food_set'], meal)
    
    
    return Response(get_meals_render_data([meal]))

@api_view(['DELETE'])
def deleteMeal(request, pk):
    if (not request.user.is_authenticated):
        message = {'message': 'User is not logged in.'}
        return Response(message)

    meal = Meal.objects.get(id=pk)
    if (meal.user != request.user):
        message = {'message': 'User is not authenticated for this data.'}
        return Response(message)

    meal.delete()

    return Response("Meal was deleted")