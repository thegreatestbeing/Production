from django.contrib import admin


from Barcode.models import SKU
from Inventory.models import Coupen, Detail, Inventory, Relation, Business
from Products.models import Category, Product, Price, Tax
from Revenue.models import Sales, Invoice

# Register your models here.
admin.site.register(Coupen)
admin.site.register(Category)
admin.site.register(Detail)
admin.site.register(Inventory)
admin.site.register(Invoice)
admin.site.register(Relation)
admin.site.register(Sales)
admin.site.register(Business)
admin.site.register(Tax)

admin.site.register(Product)

# class Price(admin.TabularInline):
#     model           = Price
#     insert_after    = 'catagory'

# class SKU(admin.TabularInline):
#     model           = SKU
#     insert_after    = 'catagory'


# class ProductAdmin(admin.ModelAdmin):
# 	fields = ('name', 'description', 'quantity', 'catagory', 'inventory')
# 	inlines = [SKU]

# admin.site.register(Product, ProductAdmin)