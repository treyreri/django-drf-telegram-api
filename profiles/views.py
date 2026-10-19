from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Profile, Avatar
from .serializers import ProfileSerializer, AvatarSerializer    

class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    search_fields = ["user__first_name", "user__last_name", "user__username"]
    def get_queryset(self):
        return Profile.objects.select_related("user").all()

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer

class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    http_method_names = ["get", "patch", "head", "options"]
    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

class AvatarListCreateView(generics.ListCreateAPIView):
    serializer_class = AvatarSerializer
    parser_classes = [MultiPartParser, FormParser]
    def get_queryset(self): return Avatar.objects.filter(profile__user=self.request.user)
    def perform_create(self, serializer):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)

class AvatarDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = AvatarSerializer
    def get_queryset(self): 
        return Avatar.objects.filter(profile__user=self.request.user)
