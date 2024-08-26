from django.urls import path

from . import views


app_name = 'mailing'

urlpatterns = [
    # mailing
    path('', views.MailingListView.as_view(), name='mailing_list'),
    path('create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),

    # message
    path('messages/', views.MessageListView.as_view(), name='messages_list'),
    path('messages/create/', views.MessageCreateView.as_view(), name='messages_create'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='messages_detail'),
    path('messages/<int:pk>/update/', views.MessageUpdateView.as_view(), name='messages_update'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='messages_delete'),
]
