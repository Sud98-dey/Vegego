from django.contrib import admin
from vegego import urls
from accounts.models import Users,Category,Product,Orders,Payment_Mode,Invoice,AssignOrder

# Register your models here.
admin.site.register(Users)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(Payment_Mode)
admin.site.register(Invoice)
admin.site.register(AssignOrder)
