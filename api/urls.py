
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('groups', GroupViewSet, basename='group')

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
]