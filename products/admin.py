from django.contrib import admin

from products.models import Basket, Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    fields = ['name', 'description']
    search_fields = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity', 'price', 'category']
    fields = ['name', 'description', ('price', 'quantity', ), 'image', 'category', 'stripe_product_price_id']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', 'price']
    list_filter = ['category']
    # readonly_fields = ['']
    list_editable = ['quantity', 'price']


class BasketAdmin(admin.TabularInline):
    model = Basket
    extra = 0
