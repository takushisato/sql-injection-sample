from django.contrib import admin

from .models import (
    Address,
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
    Review,
)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("name", "description")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "postal_code", "is_default")
    search_fields = ("user__username", "full_name", "postal_code")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    inlines = [CartItemInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating",)
