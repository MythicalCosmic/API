from django.db import models
from django.contrib.auth.models import Group, Permission
class Customers(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name


class Doctors(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    savedM = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    typeOf = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_of_service = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.price is None and self.service and self.service.price:
            self.price = self.service.price

        super().save(*args, **kwargs)

        half_price = self.price // 2
        self.doctor.savedM += half_price
        self.doctor.save()

        Money.objects.create(
            customer=self.customer,
            doctor=self.doctor,
            service=self.service,
            price=half_price
        )

    def __str__(self):
        return self.customer.full_name
#fist time

class Money(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.customer.full_name} - {self.service.name} - {self.price}'

class CustomGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=("permissions"),
    )
    def __str__(self):
        return self.name


class MainUsers(models.Model):
    full_name = models.CharField(max_length=150, unique=True)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    role = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class CashBoxLog(models.Model):
    action = models.CharField(max_length=255)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} - {self.amount} at {self.timestamp}"