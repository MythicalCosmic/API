from django.contrib.auth import authenticate, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    LoginSerializer, MoneySerializer, OrderSerializer, DoctorSerializer, ServiceSerializer,
    PermissionSerializer, CustomerSerializer, UsersMainSerializer, CategorySerializer, CashBoxLogSerializer, GroupSerializer, RoleCreateUpdateSerializer
)
from .models import Orders, Money, Service, Doctors, Customers, Category, CashBoxLog, User
from django.contrib.auth.models import Group, Permission
from rest_framework import status
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from datetime import datetime
import http.client
import urllib
import logging
from .utils import IsInGroup


logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = '7128976453:AAErFxgbb5i2LWFzra0hblV9oAyFwZwXPQY'
CHAT_ID = ['5274295129', '7127361294']



@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'server': 'You have successfully logged out!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def allOrders(request):
    request.required_group = 'Kassir'
    orders = Orders.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getAvailableDoctors(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return Response({'error': 'Service not found'}, status=404)

    doctors = service.doctors.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createOrder(request):
    print("Request Data:", request.data)
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        print("Instance Saved:", instance)
        return Response(OrderSerializer(instance).data, status=201)
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_order(request, pk):
    try:
        order = Orders.objects.get(pk=pk)
    except Orders.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    order.delete()
    return Response({'success': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_order(request, pk):
    try:
        order = Orders.objects.get(pk=pk)
    except Orders.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getAllServices(request):
    all_data = Service.objects.all()
    serializer = ServiceSerializer(all_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def addService(request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteService(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
    service.delete()
    return Response({'success': 'Service deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def updateService(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ServiceSerializer(service, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getAllDoctors(request):
    all_data = Doctors.objects.all()
    serializer = DoctorSerializer(all_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def addDoctor(request):
    serializer = DoctorSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response({'success': 'Doctor added successfully'}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def deleteDoctor(request, pk):
    try:
        doctor = Doctors.objects.get(pk=pk)
    except Doctors.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
    doctor.delete()
    return Response({'success': 'Doctor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def updateDoctor(request, pk):
    try:
        doctor = Doctors.objects.get(pk=pk)
    except Doctors.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DoctorSerializer(doctor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def allCustomers(request):
    customers = Customers.objects.all()
    serialized = CustomerSerializer(customers, many=True)
    return Response(serialized.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def createCustomer(request):
    serialized = CustomerSerializer(data=request.data)
    if not serialized.is_valid():
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    serialized.save()
    return Response({'success': 'Customer created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def updateCustomer(request, pk):
    try:
        customer = Customers.objects.get(pk=pk)
    except Customers.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteCustomer(request, pk):
    try:
        customer = Customers.objects.get(pk=pk)
    except Customers.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    customer.delete()
    return Response({'success': 'Customer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def showCashBox(request):
    try:
        cashbox_logs = CashBoxLog.objects.all().order_by('-timestamp')
        serializer = CashBoxLogSerializer(cashbox_logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getTotal(request):
    total_price = Money.objects.aggregate(total_price=Sum('price'))['total_price'] or 0
    return Response({'total_price': total_price}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_cashbox(request):
    user = request.user
    total_price_before = Orders.objects.aggregate(total_price=Sum('price'))['total_price'] or 0
    Money.objects.all().delete()
    Orders.objects.update(price=0)
    CashBoxLog.objects.create(action="reset", amount=0, comment="Cashbox reset")
    total_price_after = Orders.objects.aggregate(total_price=Sum('price'))['total_price'] or 0
    reset_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = (
        f"💸 Cashbox reset successfully\n"
        f"👤 Performed by: {user.username}\n"
        f"🕔 Time: {reset_time}\n"
        f"💰 Total price before reset: {total_price_before}\n"
        f"💰 Total price after reset: {total_price_after}"
    )
    send_telegram_message(message)
    return Response({'message': message, 'total_price': total_price_after}, status=status.HTTP_200_OK)


def send_telegram_message(message):
    conn = http.client.HTTPSConnection("api.telegram.org")
    params = urllib.parse.urlencode({
        'chat_id': CHAT_ID,
        'text': message
    })
    url = f"/bot{TELEGRAM_BOT_TOKEN}/sendMessage?{params}"
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data


@api_view(['POST'])
def withdraw_money(request):
    user = request.user
    amount = request.data.get('amount')
    comment = request.data.get('comment', '')

    if not amount or amount <= 0:
        return Response({'error': 'Invalid amount specified'}, status=status.HTTP_400_BAD_REQUEST)

    total_money = Money.objects.aggregate(total_price=Sum('price'))['total_price'] or 0
    if amount > total_money:
        return Response({'error': 'Insufficient funds in cashbox'}, status=status.HTTP_400_BAD_REQUEST)

    remaining_amount = amount
    while remaining_amount > 0:
        money_entry = Money.objects.first()
        if money_entry is None:
            break

        if money_entry.price >= remaining_amount:
            money_entry.price -= remaining_amount
            money_entry.save()
            remaining_amount = 0
        else:
            remaining_amount -= money_entry.price
            money_entry.delete()

    CashBoxLog.objects.create(action="withdraw", amount=amount, comment=comment)

    new_total = Money.objects.aggregate(total_price=Sum('price'))['total_price'] or 0
    withdraw_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = (
        f"💸 Money withdrawn successfully\n"
        f"👤 Performed by: {user.username}\n"
        f"🕔 Time: {withdraw_time}\n"
        f"💰 Amount withdrawn: {amount}\n"
        f"💰 Remaining balance: {new_total}\n"
        f"📝 Comment: {comment}"
    )
    send_telegram_message(message)

    return Response({
        'message': f'{amount} withdrawn successfully',
        'remaining_balance': new_total
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def createUser(request):
    try:
        serializer = UsersMainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'User added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error occurred while creating User', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def allUsers(request):
    users = User.objects.all()
    serialized = UsersMainSerializer(users, many=True)
    return Response(serialized.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteUser(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({'success': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def updateUser(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsersMainSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def AllCategory(request):
    categories = Category.objects.all()
    serialized = CategorySerializer(categories, many=True)
    return Response(serialized.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def createCategory(request):
    try:
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'success': 'Category added successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': 'Error occurred while creating Category', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def updateCategory(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteCategory(request, pk):
    try:
        categories = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    categories.delete()
    return Response({'success': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def allRoles(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def createRole(request):
    serializer = RoleCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        role = serializer.save()
        role.permissions.set(request.data.get('permissions', []))
        return Response(GroupSerializer(role).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editRole(request, pk):
    role = get_object_or_404(Group, pk=pk)
    serializer = RoleCreateUpdateSerializer(role, data=request.data)
    if serializer.is_valid():
        role = serializer.save()
        role.permissions.set(request.data.get('permissions', []))
        return Response(GroupSerializer(role).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteRole(request, pk):
    role = get_object_or_404(Group, pk=pk)
    role.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def listPermissions(request):
    permissions = Permission.objects.all()
    serializer = PermissionSerializer(permissions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
