from django.urls import path

from . import views


app_name = 'clients'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='clients_list'),
    path('create/', views.ClientCreateView.as_view(), name='clients_create'),
    path('<int:pk>/', views.ClientDetailView.as_view(), name='clients_detail'),
    path('<int:pk>/update/', views.ClientUpdateView.as_view(), name='clients_update'),
    path('<int:pk>/delete/', views.ClientDeleteView.as_view(), name='clients_delete'),
]
