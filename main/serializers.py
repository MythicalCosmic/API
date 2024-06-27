from rest_framework import serializers
from django.contrib.auth.models import User, Permission
from .models import Doctors, Orders, Service, Money, Customers, CustomGroup, MainUsers, Category

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    doctor = serializers.SerializerMethodField()
    service = serializers.StringRelatedField()

    class Meta:
        model = Orders
        fields = ['id', 'price', 'customer', 'doctor', 'service']

    def get_doctor(self, obj):
        return obj.doctor.full_name
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['id', 'full_name', 'specialization']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'customer', 'customer_name', 'doctor', 'doctor_name', 'service', 'service_name']  # Include other fields from Orders model as needed

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer'] = CustomerSerializer(instance.customer).data
        representation['doctor'] = DoctorSerializer(instance.doctor).data
        representation['service'] = ServiceSerializer(instance.service).data
        return representation


class ServiceSerializer(serializers.ModelSerializer):
    category_type = serializers.CharField(source='typeOf.name', read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'category_type']



class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'

class MoneySerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = Money
        fields = ['id', 'price', 'customer', 'customer_name', 'doctor', 'doctor_name', 'service']  # Include other fields from Money model as needed

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer'] = CustomerSerializer(instance.customer).data
        representation['doctor'] = DoctorSerializer(instance.doctor).data
        representation['service'] = ServiceSerializer(instance.service).data
        return representation

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name']

class CustomGroupSerializers(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Permission.objects.all(),
        source='permissions'
    )

    class Meta:
        model = CustomGroup
        fields = ['id', 'name', 'permissions', 'permission_ids']

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions', None)
        group = CustomGroup.objects.create(**validated_data)
        if permissions_data:
            group.permissions.set(permissions_data)
        group.save()
        return group


class UsersMainSerializer(serializers.ModelSerializer):
    role = CustomGroupSerializers(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomGroup.objects.all(),
        source='role',
        write_only=True
    )

    class Meta:
        model = MainUsers
        fields = ['id', 'full_name', 'age', 'address', 'phone_number', 'role', 'role_id']

    def create(self, validated_data):
        user = MainUsers.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.age = validated_data.get('age', instance.age)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        if 'role' in validated_data:
            instance.role = validated_data['role']
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'