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
    class Meta:
        model = Orders
        fields = '__all__'



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'




class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'

class MoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Money
        fields = '__all__'


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