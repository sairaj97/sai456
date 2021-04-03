
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi




router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('groups', GroupViewSet, basename='group')



schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.myapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@sairaj.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
#    path('users', UserListView.as_view(), name='users'),
    path('admins', AdminRegistrationView.as_view(), name='admins'),
    path('user/<int:id>/', UsersListView.as_view(), name ='user_edit'),
    path('user/', UsersListView.as_view(), name ='user_list'),
    path('task/', TaskListView.as_view(), name ='task_list'),
#    path('group/', GroupListView.as_view(), name ='group_list'),
#    path('group/<int:id>/', GroupListView.as_view(), name ='group_edit'),
    path('', include(router.urls)),
    path('apidoc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]