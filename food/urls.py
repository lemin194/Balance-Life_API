
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

from rest_framework.authtoken import views as rest_view

urlpatterns = [
    path('accounts/profile/', views.user_profile_view, name='user_profile'),
    path('accounts/profile/<str:pk>/upload_profile_image/', views.uploadProfileImage, name='upload_profile_image'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/<str:pk>/add_specialist', views.add_specialist, name='add_specialist'),
    path('accounts/<str:pk>/add_customer', views.add_customer, name='add_customer'),
    path('get_users/', views.get_users, name="user_profiles"),
    path('load_data/', views.loadData, name='load_data'),
    path('load_ingredients_data/', views.loadIngredientsData, name='load_ingredients'),
    path('load_nutrients_data/', views.loadNutrientsData, name='load_nutrients'),
    path('load_sample_foods_data/', views.loadSampleFoodsData, name='load_sample_foods'),
    path('', views.getRoutes, name='get_routes'),
    path('nutrients/', views.getNutrients, name='get_nutrients'),
    path('nutrients/<str:pk>/', views.getNutrient, name='get_nutrient'),
    path('ingredients/', views.getIngredients, name='get_ingredients'),
    path('ingredients/<str:pk>/', views.getIngredient, name='get_ingredient'),
    path('foods/', views.getFoods, name='get_foods'),
    path('foods/create/', views.createFood, name='create_food'),
    path('foods/<str:pk>/', views.getFood, name='get_food'),
    path('foods/<str:pk>/update/', views.updateFood, name='update_food'),
    path('foods/<str:pk>/upload_image/', views.uploadFoodImage, name='upload_food_image'),
    path('foods/<str:pk>/delete/', views.deleteFood, name='delete_food'),
    path('meals/', views.getMeals, name='get_meals'),
    path('meals/bydate/', views.getMealsByDate, name='get_meals'),
    path('meals/byweek/', views.getMealsByWeek, name='get_meals'),
    path('meals/create/', views.createMeal, name='create_meal'),
    path('meals/<str:pk>/update/', views.updateMeal, name='update_meal'),
    path('meals/<str:pk>/delete/', views.deleteMeal, name='delete_meal'),
    path('meals/<str:pk>/', views.getMeal, name='get_meal'),
]


urlpatterns += [
    # path('accounts/login/', rest_view.obtain_auth_token),
]