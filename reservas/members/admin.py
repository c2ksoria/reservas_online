from django.contrib import admin

# Register your models here.

from members.models import Members

admin.site.register(Members)