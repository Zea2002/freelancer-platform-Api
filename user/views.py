from django.contrib.auth import get_user_model,login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from .serializers import (RegisterSerializer, UserLoginSerializer,
                          UpdateProfileSerializer, ChangePasswordSerializer, 
                          FreelancerProfileSerializer, ClientProfileSerializer, 
                          SkillSerializer)
from .models import FreelancerProfile, Skill, ClientProfile
from .pagination import FreelancerPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

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

            # Create activation link
            activation_link = reverse('activate', kwargs={'uid64': uid, 'token': token})
            confirm_link = f"http://{request.get_host()}{activation_link}"

            
            email_subject = "Confirm Your Email"
            email_body = render_to_string('activation_email.html', {'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response("Check your email for confirmation.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Account activation view
def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Redirect to frontend login page after successful activation
        frontend_domain = request.get_host()
        frontend_login_url = f"http://{frontend_domain}/login"
        return redirect(frontend_login_url)
    else:
        frontend_domain = request.get_host()
        frontend_register_url = f"http://{frontend_domain}/register"
        return redirect(frontend_register_url)

class UserLoginApiView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(username=email, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)  
                return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        frontend_domain = request.get_host()
        frontend_login_url = f"http://{frontend_domain}/login"
        return redirect(frontend_login_url)

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

# ViewSets for profiles and skills
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
