from django.contrib import admin
from .models import Meal, Food, Ingredient, Nutrient, NutrientInstance, FoodInstance, IngredientInstance, User

# Register your models here.

class NutrientInstanceInline(admin.TabularInline):
    model = NutrientInstance
    extra = 1
class NutrientInline(admin.TabularInline):
    model = Nutrient
    extra = 1
class IngredientInstanceInline(admin.TabularInline):
    model = IngredientInstance
    extra = 1
class FoodInstanceInline(admin.TabularInline):
    model = FoodInstance
    extra = 1
    


class NutrientAdmin(admin.ModelAdmin):
    list_display = ('nutrient_name', 'rda', 'required', 'category')
    search_fields = ['nutrient_name', 'category']
    list_filter = ['category']

class IngredientAdmin(admin.ModelAdmin):
    inlines = [NutrientInstanceInline]
    list_display = ('ingredient_name', 'calories', 'proteins', 'fat', 'carbohydrates')
    search_fields = ['ingredient_name']
    list_filter = ['ingredient_name', 'calories', 'proteins', 'fat', 'carbohydrates']
class FoodAdmin(admin.ModelAdmin):
    inlines = [IngredientInstanceInline]
    list_display = ('food_name', 'image')
    search_fields = ['food_name']

class MealAdmin(admin.ModelAdmin):
    inlines = [FoodInstanceInline]
    list_display = ('title', 'time')
    search_fields = ['title', 'time']



admin.site.register(User)

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Nutrient, NutrientAdmin)