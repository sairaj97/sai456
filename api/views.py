from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.permissions import BasePermissionMetaclass
from django.contrib.auth.models import PermissionsMixin
from .serializers import *
from .permissions import IsSuperUser
from .models import *
from rest_framework import generics, mixins, viewsets


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)

""" Below view is optional"""
class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)


class AdminRegistrationView(APIView):
    serializer_class = AdminRegistrationSerializer
    permission_classes = (IsSuperUser, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Admin successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)




class UserViewSet(viewsets.ModelViewSet):
    """
    This view is optional.
    """
    queryset = User.objects.all()
    serializer_class = AdminsUserSerializer
    permission_classes = [IsSuperUser]




class GroupViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """

    queryset = Group.objects.all()
    serializer_class = GroupUserSerializer
    permission_classes = [IsSuperUser]

#    filter_backends = [filters.OrderingFilter]
 #   ordering_fields = ['release_date']

class UsersListView(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
#    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsSuperUser]



    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

#    def post(self, request):
#        return self.create(request)

#    def perform_create(self, serializer):
#        serializer.save(created_by=self.request.user)

    def put(self, request, id=None):
        return self.update(request, id)

    def perform_update(self, serializer):
        print(self.request.user)
        serializer.save(created_by=self.request.user)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsSuperUser]



"""
class UsersListView(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
#    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]


    def get(self, request, id=None):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        elif id:
            return self.retrieve(request, id)
        else:
            return self.list(request)


#    def post(self, request):
#        return self.create(request)

#    def perform_create(self, serializer):
#        serializer.save(created_by=self.request.user)

    def put(self, request, id=None):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            return self.update(request, id)

    def perform_update(self, serializer):
        print(self.request.user)
        serializer.save(created_by=self.request.user)

    def delete(self, request, id=None):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            return self.destroy(request, id)





    


        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
         serializer = self.serializer_class(data=request.data)
         valid = serializer.is_valid(raise_exception=True)

         if valid:
             serializer.save()
             status_code = status.HTTP_201_CREATED

             response = {
                 'success': True,
                 'statusCode': status_code,
                'message': 'Admin successfully registered!',
                'user': serializer.data
             }

             return Response(response, status=status_code)"""