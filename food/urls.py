
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('accounts/profile/', views.user_profile_view, name='user_profile'),
    path('accounts/register/', views.register_view, name='register'),
    # path('login/', views.login_view, name="login"),
    # path('logout/', LogoutView.as_view(next_page='/'),name='logout'),
    path('load_data/', views.loadData, name='load_data'),
    path('load_foods_data/', views.loadFoodsData, name='load_foods'),
    path('load_nutrients_data/', views.loadNutrientsData, name='load_nutrients'),
    path('', views.getRoutes, name='get_routes'),
    path('nutrients/', views.getNutrients, name='get_nutrients'),
    path('nutrients/<str:pk>/', views.getNutrient, name='get_nutrient'),
    path('foods/', views.getFoods, name='get_foods'),
    path('foods/<str:pk>/', views.getFood, name='get_food'),
    path('meals/', views.getMeals, name='get_meals'),
    path('meals/bydate/', views.getMealsByDate, name='get_meals'),
    path('meals/byweek/', views.getMealsByWeek, name='get_meals'),
    path('meals/create/', views.createMeal, name='create_meal'),
    path('meals/<str:pk>/update/', views.updateMeal, name='update_meal'),
    path('meals/<str:pk>/delete/', views.deleteMeal, name='delete_meal'),
    path('meals/<str:pk>/', views.getMeal, name='get_meal'),
]
