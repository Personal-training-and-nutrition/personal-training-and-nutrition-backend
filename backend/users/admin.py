from django.contrib import admin
from .models import Specialist, User, SpecialistUser, Specialization

admin.site.register(Specialist)
admin.site.register(User)
admin.site.register(SpecialistUser)
admin.site.register(Specialization)
