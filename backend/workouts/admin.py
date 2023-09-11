from django.contrib import admin
from .models import (Exercise,
                     ExercisesList,
                     TrainingExercisesList,
                     Training,
                     TrainingPlan,
                     TrainingType)

admin.site.register(Exercise)
admin.site.register(Training)
admin.site.register(TrainingPlan)
admin.site.register(TrainingType)
admin.site.register(TrainingExercisesList)
admin.site.register(ExercisesList)
