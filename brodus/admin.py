from django.contrib import admin
from .models import Jobs, Workers, Proj, Idioma, Lenguaje, MyUser
# Register your models here.
admin.site.register(Jobs)
admin.site.register(Workers)
admin.site.register(Proj)
admin.site.register(Idioma)
admin.site.register(Lenguaje)
admin.site.register(MyUser)
