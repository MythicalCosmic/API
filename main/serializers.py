from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from .models import Doctors, Orders, Service, Money, Customers, Category, CashBoxLog

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['id', 'full_name', 'specialization']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customers.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctors.objects.all())
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Orders
        fields = ['id', 'customer', 'doctor', 'service', 'price']

    def create(self, validated_data):
        if 'price' not in validated_data or validated_data['price'] is None:
            validated_data['price'] = validated_data['service'].price_of_service
        return super().create(validated_data)

class ServiceSerializer(serializers.ModelSerializer):
    typeOf = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Service
        fields = ['id', 'name', 'typeOf', 'price_of_service']

class MoneySerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)

    class Meta:
        model = Money
        fields = ['id', 'price', 'customer', 'customer_name', 'doctor', 'doctor_name', 'service']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class UsersMainSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source='groups', write_only=True)
    role = serializers.StringRelatedField(source='groups.first', many=False)
    age = serializers.IntegerField(source='profile.age', required=False)
    address = serializers.CharField(source='profile.address', required=False)
    phone_number = serializers.CharField(source='profile.phone_number', required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'age', 'address', 'phone_number', 'group', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        group = validated_data.pop('groups')
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        user.groups.set([group])
        if password:
            user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)  # Ensure Profile model is imported
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        group = validated_data.pop('groups', None)
        instance = super(UsersMainSerializer, self).update(instance, validated_data)
        if group:
            instance.groups.set([group])
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()

        # Update profile fields
        profile = instance.profile  # Ensure Profile model is imported
        profile.age = profile_data.get('age', profile.age)
        profile.address = profile_data.get('address', profile.address)
        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.save()

        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CashBoxLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBoxLog
        fields = ['action', 'amount', 'timestamp', 'comment']

class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all()
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']
