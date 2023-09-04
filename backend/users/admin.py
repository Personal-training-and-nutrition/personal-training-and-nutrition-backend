from django.contrib import admin
from .models import (Specialist, User, SpecialistUser,
                     Specialization, Gender, DemographicUser, Role)

admin.site.register(Specialist)
admin.site.register(Gender)
admin.site.register(User)
admin.site.register(DemographicUser)
admin.site.register(SpecialistUser)
admin.site.register(Specialization)
admin.site.register(Role)
