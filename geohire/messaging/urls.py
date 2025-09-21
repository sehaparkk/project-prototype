from django.urls import path
from . import views

urlpatterns = [
    path('send/<int:receiver_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('view/<int:message_id>/', views.view_message, name='view_message'),
]