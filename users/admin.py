from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']
    list_display_links = ['id', 'username']
    search_fields = ['id', 'username', 'first_name', 'last_name']
    inlines = [BasketAdmin]


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration']
    readonly_fields = ['created_at']
    search_fields = ['user', 'created_at']
