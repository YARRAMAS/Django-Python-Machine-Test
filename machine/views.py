from django.shortcuts import render
from rest_framework import status, viewsets,permissions
from .models import Client, Project, ProjectAssignment
from .serializers import ClientSerializer, ProjectSerializer, ProjectAssignmentSerializer
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response                                                                                                                
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.decorators import api_view

def home(request):
    return HttpResponse("Hello World")

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]  # Enforce authentication

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_at=datetime.now()
        )

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('users')
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        client_id = self.request.data.get('client_id')
        client = Client.objects.get(id=client_id)
        serializer.save(client=client)
        

class ProjectAssignView(APIView):

    def post(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({"detail": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        project_name = request.data.get('project_name')
        users_data = request.data.get('users', [])

        # Validate project name and user IDs
        if not project_name:
            return Response({"detail": "Project name is required"}, status=status.HTTP_400_BAD_REQUEST)

        invalid_user_ids = []
        for user_data in users_data:
            user_id = user_data.get('id')
            if not user_id:
                invalid_user_ids.append(user_data)
        if invalid_user_ids:
            return Response({"detail": "Invalid user IDs: {}".format(invalid_user_ids)}, status=status.HTTP_400_BAD_REQUEST)

        # Create the project
        project = Project.objects.create(project_name=project_name, client=client, created_by=request.user)

        # Assign users to the project
        for user_data in users_data:
            user_id = user_data.get('id')
            try:
                user = User.objects.get(id=user_id)
                project.users.add(user)
            except User.DoesNotExist:
                return Response({"detail": f"User with ID {user_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        project_serializer = ProjectSerializer(project)
        return Response(project_serializer.data, status=status.HTTP_201_CREATED)
    
class ProjectAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ProjectAssignment.objects.all()
    serializer_class = ProjectAssignmentSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'])
    def assign_user_to_project(self, request, pk=None):
        project = self.get_object()
        user = User.objects.get(id=request.data['user_id'])
        assignment, created = ProjectAssignment.objects.get_or_create(project=project, user=user)

        if created:
            return Response({"message": "User assigned to project successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User already assigned to this project"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def assigned_projects_for_user(self, request):
        user = request.user
        assignments = ProjectAssignment.objects.filter(user=user)
        serializer = ProjectAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_project(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
        logger.debug(f"Client found: {client.client_name}")
    except Client.DoesNotExist:
        return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    logger.debug(f"Request User: {request.user.username}")

    data = request.data
    project_name = data.get('project_name')
    users = data.get('users', [])

    # Create project
    project = Project.objects.create(
        project_name=project_name,
        client=client,
        created_by=request.user  # Assuming the request user is logged in
    )
    logger.debug(f"Project created: {project.project_name}")

    # Assign users to the project
    for user_data in users:
        try:
            user = User.objects.get(id=user_data['id'])
            project.users.add(user)
        except User.DoesNotExist:
            return Response({"error": f"User with id {user_data['id']} not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_projects(request):
    user = request.user
    projects = Project.objects.filter(users=user)
    return Response(ProjectSerializer(projects, many=True).data)

@api_view(['GET'])
def client_detail(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Fetch the client with the associated projects
    projects = client.projects.all()
    return Response({
        'id': client.id,
        'client_name': client.client_name,
        'created_at': client.created_at,
        'created_by': client.created_by.username,
        'projects': ProjectSerializer(projects, many=True).data
    })
    
@api_view(['PUT', 'PATCH'])
def update_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data
    project.project_name = data.get('project_name', project.project_name)
    project.save()
    
    return Response(ProjectSerializer(project).data)

@api_view(['DELETE'])
def delete_project(request, client_id, project_id):
    try:
        client = Client.objects.get(id=client_id)
        project = Project.objects.get(id=project_id, client=client)
    except (Client.DoesNotExist, Project.DoesNotExist):
        return Response({"error": "Client or Project not found"}, status=status.HTTP_404_NOT_FOUND)

    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)