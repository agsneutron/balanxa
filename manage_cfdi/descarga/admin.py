from django.contrib import admin

from .models import *

class accessKey(admin.ModelAdmin):
	list_display = ('access_description','access_key')
	list_per_page = 25
	ordering = ['-access_id', 'access_key']

admin.site.register(ApiTbAccess,accessKey)