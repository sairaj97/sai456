from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )

    def create(self, validated_data):
        auth_user = User.objects.create_superuser(**validated_data)
        return auth_user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'role'
        )


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = [
            'id',
            'user',
            'text'
        ]
        read_only_fields = ('user',)


class GroupUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
 #   tasks = TaskSerializer(many=True)
 #   users = AdminsUserSerializer(many=True)


    class Meta:
        model = Group
        fields = ( 'id','name', 'users')
        extra_kwargs = {'users': {'required': False}}

 #       read_only_fields = ('tasks',)


class AdminsUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    tasks = TaskSerializer(many=True)
    group = GroupUserSerializer(many=True)

#    password = serializers.CharField(
 #       write_only=True, required=True)

    class Meta:
        model = User
        fields = ( 'id',
            'email', 'role',
            'is_active', 'tasks', 'group')

        extra_kwargs = {'group': {'required': False}}


class AdminUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    tasks = TaskSerializer(many=True)

#    password = serializers.CharField(
 #       write_only=True, required=True)

    class Meta:
        model = User
        fields = ( 'id',
            'email', 'role',
            'is_active', 'tasks', 'group', 'is_superuser')
        extra_kwargs = {'groups': {'required': False}}

    def create(self, validated_data):
        tasks = validated_data.pop('tasks')
        #tags = validated_data.pop('tags')
        user = User.objects.create(**validated_data)
        for task in tasks:
            Task.objects.create(**task, user=user)
        #user.tags.set(tags)
        return user

    def update(self, instance, validated_data):
        tasks = validated_data.pop('tasks')
        keep_tasks = []
        for task in tasks:
            if "id" in task.keys():
                if Task.objects.filter(id=task["id"]).exists():
                    c = Task.objects.get(id=task["id"])
                    c.text = task.get('text', c.text)
                    c.save()
                    keep_tasks.append(c.id)
                else:
                    continue
            else:
                c = Task.objects.create(**task, user=instance)
                keep_tasks.append(c.id)

        for task in instance.tasks:
            if task.id not in keep_tasks:
                task.delete()

        return instance