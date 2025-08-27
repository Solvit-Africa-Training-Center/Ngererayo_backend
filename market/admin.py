from django.contrib import admin

from .models import Product,Cart,CartItem,Order,Owner,ProductComments,ProductMessage

# Register your models here.



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'owner', 'price', 'quantity','description','product_image']
    list_filter = ['owner', 'price']
    search_fields = ['product_name', 'description']
    list_per_page = 10




@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'farming_name', 'location']
    search_fields = ['user__username', 'farming_name']
    list_per_page = 10
    



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']
    list_per_page = 10



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__user__username', 'product__name']
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart', 'created_at', 'address']
    # search_fields = ('user__username', 'product__name', 'address')
    list_per_page = 10



@admin.register(ProductMessage)
class ProductMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'product', 'message', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'product__name', 'message']
    list_per_page = 10



@admin.register(ProductComments)
class ProductCommentsAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'comment', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    list_per_page = 10
