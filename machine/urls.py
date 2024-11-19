from django.urls import path,include
from django.contrib import admin
from . import views
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet, ProjectAssignmentViewSet
from .views import ProjectAssignView

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project_assignments', ProjectAssignmentViewSet)

urlpatterns=[
    
    path("api/",include(router.urls)),
    path('',views.home,name="home"),
    path('',include(router.urls)), 
    #path('clients/<int:client_id>/projects/', ProjectAssignView.as_view(), name='assign-project'),   
    path('clients/<int:client_id>/projects/', views.create_project),   
    path('projects/', views.list_projects),          
    path('clients/<int:client_id>/', views.client_detail),
    path('projects/<int:project_id>/', views.update_project),
    path('clients/<int:client_id>/projects/<int:project_id>/', views.delete_project),
    ]
