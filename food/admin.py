from django.contrib import admin
from .models import Meal, Food, Nutrient, NutrientCategory

# Register your models here.

admin.site.register(Food)
admin.site.register(Meal)


class NutrientInline(admin.TabularInline):
    model = Nutrient
    extra = 1

class NutrientAdmin(admin.ModelAdmin):
    list_display = ('name', 'rda', 'required', 'category')
    search_fields = ['name']
    list_filter = ['_category__category_name']

class NutrientCategoryAdmin(admin.ModelAdmin):
    inlines = [NutrientInline]
    search_fields = ['category_name']


admin.site.register(Nutrient, NutrientAdmin)
admin.site.register(NutrientCategory, NutrientCategoryAdmin)