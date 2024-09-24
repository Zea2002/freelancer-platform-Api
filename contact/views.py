from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer
from rest_framework.permissions import AllowAny

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # Custom success message
            return Response({"message": "Your message has been sent!"}, status=status.HTTP_201_CREATED, headers=headers)
        # Custom error message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
