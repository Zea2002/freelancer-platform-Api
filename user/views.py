from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import status, views,viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer, UpdateProfileSerializer, ChangePasswordSerializer, FreelancerProfileSerializer,ClientProfileSerializer,SkillSerializer
from .models import FreelancerProfile, Skill,ClientProfile
from .pagination import FreelancerPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect

User = get_user_model()

class RegisterView(views.APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            # Generate token and UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Debugging: print UID and token to ensure they are correct
            print(f"UID: {uid}, Token: {token}")

            # Try generating activation link using reverse
            try:
                activation_link = reverse('activate', kwargs={'uid64': uid, 'token': token})
                confirm_link = f"http://{request.get_host()}{activation_link}"
            except Exception as e:
                print(f"Error generating URL: {e}")
                return Response({"error": "Error generating activation link"}, status=400)

            # Prepare and send email
            email_subject = "Confirm Your Email"
            email_body = render_to_string('activation_email.html', {'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response("Check your email for confirmation.")
        return Response(serializer.errors)

def activate(request, uid64, token):
    try:
        # Decode UID from base64
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if token is valid
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # Log the user in (session-based)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    def post(self, request):
        logout(request) 
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK),redirect('login')

class UpdateProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data['old_password']
            new_password = serializer.data['new_password']

            if not request.user.check_password(old_password):
                return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            request.user.set_password(new_password)
            request.user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ClientProfileViewSet(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer

class FreelancerProfileViewSet(viewsets.ModelViewSet):
    queryset = FreelancerProfile.objects.all()
    serializer_class = FreelancerProfileSerializer
    pagination_class = FreelancerPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['skills']  
    search_fields = ['skills__name']
    def get_queryset(self):
        queryset = FreelancerProfile.objects.all()
        skill_slug = self.request.query_params.get('skill', None)
        if skill_slug:
            skill = Skill.objects.filter(slug=skill_slug).first()
            if skill:
                queryset = queryset.filter(skills=skill)
        return queryset


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer