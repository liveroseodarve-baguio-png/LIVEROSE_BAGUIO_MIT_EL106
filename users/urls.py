# urlpatterns = [
#     # UI routes
#     path('register/', views.register_ui, name='register_ui'),
#     path('login/', views.login_ui, name='login_ui'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('logout/', views.logout_ui, name='logout_ui'),
#     path('activate/<uidb64>/<token>/', views.activate, name='activate'),

# ]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_ui, name='register_ui'),
    path('login/', views.login_ui, name='login_ui'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_ui, name='logout_ui'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
