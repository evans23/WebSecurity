from django.contrib import admin

from .models import BankAccount, Profile, RsaQuestion, TheWorldIsOver

# Register your models here.

admin.site.register(BankAccount)
admin.site.register(TheWorldIsOver)
admin.site.register(Profile)
admin.site.register(RsaQuestion)
