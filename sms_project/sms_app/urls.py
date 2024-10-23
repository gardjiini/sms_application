from django.urls import path
from .views import index, callback, fetch_sms_callbacks

urlpatterns = [
    path('', index, name='index'),  # Add the index view for SMS form
    path('callback/', callback, name='callback'),
    path('fetch_sms_callbacks/', fetch_sms_callbacks, name='fetch_sms_callbacks'),
]
