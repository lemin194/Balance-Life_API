from rest_framework.serializers import ModelSerializer
from .mscript import *
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )

# Register Serializer
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])

        return user

class NutrientSerializer(ModelSerializer):
    class Meta:
        model = Nutrient
        fields = '__all__'

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        
class FoodSerializer(ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'
        
class MealSerializer(ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'