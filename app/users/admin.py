from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_staff', 'is_active')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    readonly_fields = ('is_staff',)
