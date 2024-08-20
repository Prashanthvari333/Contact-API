from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Contact
from .serializers import ContactSerializer
from django.db.models import Q, Count
from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.spam.models import SpamReport
# Create your views here.

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_contact(request):
    x = request.data
    print("name : ",request.data.get('add_by'))
    user = User.objects.get(phone_number = request.data.get('add_by'))
    contact = Contact.objects.create(
                    user=user,
                    name=x.get('name'),
                    phone_number= x.get('phone_number'),
                    email= x.get('email')
                )
    if contact:
        return Response({"message": "Contact added successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Failed to add contact"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def contact_list(request):
    if request.method == 'GET':
        contacts = Contact.objects.filter(user=request.user)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def contact_detail(request, pk):
    try:
        contact = Contact.objects.get(pk=pk, user=request.user)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_contacts(request):
    query = request.query_params.get('q', '')
    search_type = request.query_params.get('type', 'name')

    if search_type == 'name':
        results = search_by_name(query)
    elif search_type == 'phone':
        results = search_by_phone(query)
    else:
        return Response({'error': 'Invalid search type'}, status=status.HTTP_404_NOT_FOUND)

    return Response(results,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_details_by_number(request,phone_number,id):
    print("User details :", request.user)
    is_registerd = False
    if User.objects.filter(phone_number=phone_number).exists():
        is_registerd = True
        
    if(request.user.is_authenticated):
        contacts = get_contacts_by_user(request.user.phone_number)
        if contacts.filter(phone_number = phone_number,id=id).exists() and User.objects.filter(phone_number=phone_number).exists():
            contact = contacts.get(phone_number = phone_number,id=id)
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        else:
            count = SpamReport.objects.filter(phone_number=phone_number).count()
            spam_likelihood = ""
            if count==0:
                spam_likelihood = "Not spam"
            elif (count<5):
                spam_likelihood = "Likly spam"
            elif (count<10):
                spam_likelihood = "Spam"
            else:
                spam_likelihood = "Top spammer"
            if is_registerd:
                user = User.objects.get(phone_number=phone_number)
                data = {
                    "name":  user.username,
                    "phone_number": user.phone_number, 
                    "spam_likelihood" : spam_likelihood ,
                    "number_of_spam_reports" : count
                }
                return Response(data,status=status.HTTP_200_OK)
            else:
                contact = contacts.get(phone_number = phone_number,id=id)            
                data = {
                    "name":  contact.name,
                    "phone_number": contact.phone_number,  
                    "spam_likelihood" : spam_likelihood ,
                    "number_of_spam_reports" : count
                }
                return  Response(data,status=status.HTTP_200_OK)

                
            
    return Response({"message":"No Contact Available"},status=status.HTTP_204_NO_CONTENT)
    
    

def search_by_name(query):
    users = User.objects.filter(
         Q(username__istartswith=query) | Q(username__icontains=query)
    )
    
    
    contacts = Contact.objects.filter(
        Q(name__istartswith=query) | Q(name__icontains=query)
    )
    # Convert QuerySet to a list and sort in Python
    contacts = list(contacts)
    contacts.sort(key=lambda contact:contact.name.lower().startswith(query.lower()), reverse=True)
    
    return [ContactSerializer(contacts, many=True).data,UserSerializer(users,many=True).data]


def search_by_phone(query):
    user = User.objects.filter(phone_number=query).first()
    if user:
        return UserSerializer(user).data

    contacts = Contact.objects.filter(phone_number=query)

    return ContactSerializer(contacts, many=True).data


def get_contacts_by_user(phone_number):
    user = User.objects.get(phone_number = phone_number)
    return Contact.objects.filter(user_id = user.id)
