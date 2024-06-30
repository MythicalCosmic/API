from django.contrib import admin
from .models import Customers, Doctors, Category, Service, Orders, CustomGroup, MainUsers, CashBoxLog
admin.site.register(Customers)
admin.site.register(Doctors)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Orders)
admin.site.register(CustomGroup)
admin.site.register(MainUsers)
admin.site.register(CashBoxLog)
