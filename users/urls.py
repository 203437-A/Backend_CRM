from django.urls import path
from .views import ClientList, ClientDetail, CategoryList, CategoryDetail, ClientCategoryList, ClientCategoryDetail, EmployeeList, EmployeeDetail, MyObtainTokenPairView


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('employees/', EmployeeList.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetail.as_view(), name='employee-detail'),
    path('clients/', ClientList.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetail.as_view(), name='client-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('client-categories/', ClientCategoryList.as_view(), name='clientcategory-list'),
    path('client-categories/<int:pk>/', ClientCategoryDetail.as_view(), name='clientcategory-detail'),
]
