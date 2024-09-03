from django.urls import path

from . import views


app_name = 'mailing'

urlpatterns = [
    # mailing
    path('', views.MailingListView.as_view(), name='mailing_list'),
    path('create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/toggle/', views.toggle_mailing, name='mailing_toggle'),

    # results
    path('<int:pk>/results/', views.ResultListView.as_view(), name='results_list'),
    path('<int:pk>/delete_result/', views.ResultDeleteView.as_view(), name='results_delete'),

    # message
    path('messages/', views.MessageListView.as_view(), name='messages_list'),
    path('messages/create/', views.MessageCreateView.as_view(), name='messages_create'),
    path('messages/<int:pk>/update/', views.MessageUpdateView.as_view(), name='messages_update'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='messages_delete'),
    
    # manager's api
    path('<int:pk>/', views.ManagerMailingListView.as_view(), name='manager_mailing_list'),
]
