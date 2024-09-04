from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import SpamReport
from .serializers import SpamReportSerializer

# Create your views here.


# to fetch all the spam contacts
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_spam_report_list(request):
    spam_reports = SpamReport.objects.all()
    serializer = SpamReportSerializer(spam_reports, many=True)
    return Response(serializer.data)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def get_spam_report_detail(request, pk):
    try:
        spam_report = SpamReport.objects.get(pk=pk)
    except SpamReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SpamReportSerializer(spam_report)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SpamReportSerializer(spam_report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        spam_report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
 
# to mark a contact as a spam report   
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_as_spam(request):
    phone_number = request.data.get('phone_number')
    description = request.data.get('description', '')

    if not phone_number:
        return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a spam report
    spam_report, created = SpamReport.objects.get_or_create(
        phone_number=phone_number,
        reported_by=request.user,
        defaults={'description': description}
    )

    if not created:
        return Response({"message": "This number has already been reported as spam by you."}, status=status.HTTP_200_OK)

    return Response({"message": "Number marked as spam successfully."}, status=status.HTTP_201_CREATED)
