from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User
from .serializers import UserSerializer
from apps.contacts.serializers import ContactSerializer
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout as django_logout
from apps.users.models import User
from apps.contacts.models import Contact
from .PhoneNumberBackend import PhoneNumberBackend
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest

# Create your views here.
@permission_classes([permissions.IsAuthenticated])
def  index(request):
    return HttpResponse("Hello User")


# to fetch all the existing registered users
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    print('is auth : ', request.user.is_authenticated)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

#to deal with individual usere
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def user_operations(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #to show user details
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    #to update user details
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # to delete user
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
 # to fetch all the contacts related to specific user
@api_view(["POST"]) 
@permission_classes([permissions.IsAuthenticated])  
def get_contacts_by_user(request):
    user = User.objects.get(phone_number = request.data.get('phone_number'))
    user_contacts = Contact.objects.filter(user_id = user.id)
    return Response(ContactSerializer(user_contacts,many=True).data)
    

# To register a new user
@csrf_exempt
@api_view(['POST'])
def register(request):
    data = request.data
    username = data.get('username')
    phone_number = data.get('phone_number')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not phone_number or not password:
        print(username , password , phone_number)
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
    
# to sigin into application
@csrf_exempt
@api_view(['POST'])
def signin(request):
    data = request.data
    phone_number = data.get('phone_number')
    password = data.get('password')

    if not phone_number or not password:
        return Response({'error': 'Phone number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    bk = PhoneNumberBackend()

    user = bk.authenticate(request, phone_number=phone_number, password=password)
    
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
    
# for logout from application
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def logout(request):
    django_logout(request)
    return Response({'message': 'Logged out successfully'}, status=204)

