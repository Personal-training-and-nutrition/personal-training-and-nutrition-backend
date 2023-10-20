from django.contrib import admin

from .models import (Education, Institution, Params, SpecialistClient,
                     Specialists, User,)

admin.site.register(Education)
admin.site.register(Institution)
admin.site.register(Params)
admin.site.register(SpecialistClient)
admin.site.register(Specialists)
admin.site.register(User)
