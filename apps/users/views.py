from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User
from .serializers import UserSerializer
from django.http import HttpResponse
from django.contrib.auth import login
from apps.users.models import User
from .PhoneNumberBackend import PhoneNumberBackend
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def  index(request):
    return HttpResponse("Hello User")


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@csrf_exempt
@api_view(['POST'])
def register(request):
    data = request.data
    print(data)
    username = data.get('username')
    phone_number = data.get('phone_number')
    password = data.get('password')
    email = data.get('email')

    if not username or not phone_number or not password:
        return Response({'error': 'Username, phone number, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    elif  User.objects.filter(phone_number=phone_number).exists():
        return Response({'error': 'phone_number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.','user' : serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Some thing went wrong.'},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
@csrf_exempt
@api_view(['POST'])
def signin(request):
    data = request.data
    print(data)
    phone_number = data.get('phone_number')
    password = data.get('password')

    if not phone_number or not password:
        return Response({'error': 'Phone number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    bk = PhoneNumberBackend()

    user = bk.authenticate(request, phone_number=phone_number, password=password)
    
    print(user)
    
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

