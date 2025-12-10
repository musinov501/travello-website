from django.urls import path
from apps.users.views.users import RegisterView, LoginView, ListUserView
from apps.users.views.device import (
    RegisterDeviceView, 
    DeviceListView,
    DeviceDetailView,
    DeviceLogoutView
)

app_name = 'users'

urlpatterns = [
   
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('list/', ListUserView.as_view(), name='list_users'),
    
    
    path('device/register/', RegisterDeviceView.as_view(), name='register_device'),
    path('device/', DeviceListView.as_view(), name='list_devices'),
    path('device/<int:id>/', DeviceDetailView.as_view(), name='device_detail'),
    path('device/<int:id>/logout/', DeviceLogoutView.as_view(), name='device_logout'),
]