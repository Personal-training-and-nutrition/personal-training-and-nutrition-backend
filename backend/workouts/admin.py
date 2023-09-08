from django.contrib import admin
from .models import (Exercise,
                     ExercisesList,
                     Exercises_list_Exercise,
                     Training,
                     TrainingPlan,
                     TrainingType)

admin.site.register(Exercise)
admin.site.register(Training)
admin.site.register(TrainingPlan)
admin.site.register(TrainingType)
admin.site.register(Exercises_list_Exercise)
admin.site.register(ExercisesList)

# Register your models here.
