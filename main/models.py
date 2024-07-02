from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username field must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=150)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name='user_groups',
        blank=True,
        help_text=_('Groups this user belongs to. A user will get all permissions granted to each of their groups.')
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions_set',
        blank=True,
        help_text=_('Specific permissions for this user.')
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'age', 'address', 'phone_number']

    def __str__(self):
        return self.username

# Additional models
class Customers(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

class Doctors(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
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
        if self.price is None or self.price == 0:
            self.price = self.service.price_of_service

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

class Money(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.customer.full_name} - {self.service.name} - {self.price}'

class CashBoxLog(models.Model):
    action = models.CharField(max_length=255)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} - {self.amount} at {self.timestamp}"
