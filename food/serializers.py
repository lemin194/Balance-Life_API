from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .mscript import *
from django.contrib.auth import get_user_model

User = get_user_model()
# User Serializer
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )


class NutrientSerializer(ModelSerializer):
    class Meta:
        model = Nutrient
        fields = '__all__'

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        
class FoodSerializer(ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Food
        fields = ('id', 'food_name', 'image')
        
class MealSerializer(ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'