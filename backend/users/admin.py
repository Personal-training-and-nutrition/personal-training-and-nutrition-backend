from django.contrib import admin
from .models import Specialist, User, SpecialistUser

admin.site.register(Specialist)
admin.site.register(User)
admin.site.register(SpecialistUser)
