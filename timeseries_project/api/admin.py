from django.contrib import admin
from .models import UseCase, Dataset, SeasonalityComponent

# Register your models here.
admin.site.register(UseCase)
admin.site.register(Dataset)
admin.site.register(SeasonalityComponent)
