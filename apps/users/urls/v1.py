from django.urls import path


from apps.users.views.users import RegisterView, LoginView, ListUserView
from apps.users.views.device import RegisterDeviceView, DeviceListView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name="login"),
    path("list/", ListUserView.as_view(), name="list_users"),
    
    path('register-device/', RegisterDeviceView.as_view(), name='register_device'),
    path('list-devices/', DeviceListView.as_view(), name='list_devices')
    
    
]


