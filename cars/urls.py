from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cars', views.CarViewSet)

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/new/', views.car_create, name='car_create'),
    path('car/<int:pk>/edit/', views.car_edit, name='car_edit'),
    path('car/<int:pk>/delete/', views.car_delete, name='car_delete'),
    path('api/', include(router.urls)),
]
