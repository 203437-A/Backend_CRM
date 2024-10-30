
from rest_framework import serializers
from .models import Client, Category, ClientCategory, Employee

# from django.contrib.auth.hashers import make_password

####
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['user_id'] = str(user.id)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone_number'] = user.phone_number
        token['is_staff'] = user.is_staff

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        data['user_id'] = str(self.user.id)
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['phone_number'] = self.user.phone_number
        data['is_staff'] = self.user.is_staff

        return data

###

from django.contrib.auth.models import Group

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','username', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is None:
            raise serializers.ValidationError({"password": "Este campo es requerido para la creación."})
        
        employee = Employee.objects.create(**validated_data)
        employee.set_password(password)
        
        if employee.is_staff:
            admin_group = Group.objects.get(name='Admin')
            admin_group.user_set.add(employee)
        else:
            employee_group = Group.objects.get(name='Empleado')
            employee_group.user_set.add(employee)
        
        employee.save()
        return employee

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        
        if instance.is_staff:
            admin_group = Group.objects.get(name='Admin')
            employee_group = Group.objects.get(name='Empleado')
            admin_group.user_set.add(instance)
            employee_group.user_set.remove(instance)
        else:
            admin_group = Group.objects.get(name='Admin')
            employee_group = Group.objects.get(name='Empleado')
            admin_group.user_set.remove(instance)
            employee_group.user_set.add(instance)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategory
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    categories_detail = CategorySerializer(source='categories', many=True, read_only=True) 
    categories = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all(),
        write_only=True 
    )

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'details', 'created_at', 'updated_at', 'categories', 'categories_detail']

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        client = Client.objects.create(**validated_data)
        client.categories.set(categories)
        return client

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if categories is not None:
            instance.categories.set(categories)
        instance.save()
        return instance

