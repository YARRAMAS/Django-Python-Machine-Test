from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project, ProjectAssignment
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Only include `id` and `username` of the user


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        # Handle AnonymousUser by assigning a default admin user
        if not user.is_authenticated:
            user = User.objects.get(username='admin')  # Replace with a valid username
            
        validated_data['updated_at'] = datetime.now()
        # Remove `created_by` from validated_data to avoid duplicate keyword argument
        validated_data.pop('created_by', None)

        # Create the Client instance with the authenticated or default user
        client = Client.objects.create(**validated_data, created_by=user)
        return client


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    
    class Meta:
        model = Project
        fields = '__all__'



class ProjectAssignmentSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    user = UserSerializer()

    class Meta:
        model = ProjectAssignment
        fields = ['id', 'project', 'user']
