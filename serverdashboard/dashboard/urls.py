''' refer to Django documentation for details
(c) Franz Ludwig Kostelezky, <info@kostelezky.com>'''

from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('wake/<int:server_id>', views.wake, name='wake'),
    path('bitmap/<int:server_id>', views.bitmap, name='bitmap')
]
