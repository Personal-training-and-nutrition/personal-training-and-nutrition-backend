from django.contrib import admin

from .models import (DietPlan, DietPlanDiet, Diets, DietsMealsList,
                     MealProduct, Meals, MealsList, MealsType, Products,)

admin.site.register(MealsType)
admin.site.register(Products)
admin.site.register(Meals)
admin.site.register(MealsList)
admin.site.register(Diets)
admin.site.register(DietPlan)
admin.site.register(DietPlanDiet)
admin.site.register(MealProduct)
admin.site.register(DietsMealsList)
