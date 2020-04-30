# Register your models here.
from django.contrib import admin

from mercanet import models


@admin.register(models.TransactionMercanet)
class BasicAdmin(admin.ModelAdmin):
    pass
