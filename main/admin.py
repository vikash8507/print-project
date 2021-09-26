from django.contrib import admin

# Register your models here.
from main.models import Voter, Payment, PANCard

admin.site.register(Voter)
admin.site.register(Payment)
admin.site.register(PANCard)