from django.contrib import admin

from .models import (Education, Gender, Institution, Params, Role,
                     SpecialistClient, Specialists, User,)

admin.site.register(Education)
admin.site.register(Gender)
admin.site.register(Institution)
admin.site.register(Params)
admin.site.register(Role)
admin.site.register(SpecialistClient)
admin.site.register(Specialists)
admin.site.register(User)
