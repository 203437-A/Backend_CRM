from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client, Category, ClientCategory, Employee
from .serializers import ClientSerializer, CategorySerializer, ClientCategorySerializer, EmployeeSerializer
from django.http import Http404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

from rest_framework.exceptions import NotFound
from .permissions import CustomEmployeePermission

class EmployeeList(APIView):
    permission_classes = [CustomEmployeePermission]

    def get(self, request, format=None):
        if request.user.is_staff:
            employees = Employee.objects.all()
        else:
            employees = Employee.objects.filter(id=request.user.id)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class EmployeeDetail(APIView):
    permission_classes = [CustomEmployeePermission]

    def get_object(self, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            self.check_object_permissions(self.request, employee)
            return employee
        except Employee.DoesNotExist:
            raise NotFound('No se encuentra el empleado.')

    def get(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=204)
   
class ClientList(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Client.objects.all()

    def get(self, request, format=None):
        clients = self.get_queryset()  
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientDetail(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Client.objects.all()
    
    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Client.DoesNotExist:
            raise NotFound(detail="Objeto no encontrado", code=404)

    def get(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CategoryList(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Category.objects.all()

    def get(self, request, format=None):
        categories = self.get_queryset() 
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    permission_classes = [DjangoModelPermissions]
    def get_queryset(self):
        return Category.objects.all()

    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound(detail="Objeto no encontrado", code=404)

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClientCategoryList(APIView):
    permission_classes = [DjangoModelPermissions]
    def get_queryset(self):
        return ClientCategory.objects.all()

    def get(self, request, format=None):
        client_categories = self.get_queryset() 
        serializer = ClientCategorySerializer(client_categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientCategoryDetail(APIView):
    permission_classes = [DjangoModelPermissions]
    def get_queryset(self):
        return ClientCategory.objects.all()

    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except ClientCategory.DoesNotExist:
            raise NotFound(detail="Objeto no encontrado", code=404)

    def get(self, request, pk, format=None):
        client_category = self.get_object(pk)
        serializer = ClientCategorySerializer(client_category)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        client_category = self.get_object(pk)
        serializer = ClientCategorySerializer(client_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        client_category = self.get_object(pk)
        client_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
