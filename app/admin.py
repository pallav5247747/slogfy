from django.contrib import admin
from .models import Apply,Job,Login_Accounts,Mcq
# Register your models here.
admin.site.register(Login_Accounts)
admin.site.register(Apply)
admin.site.register(Job)
admin.site.register(Mcq)