from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from apps.main.permissions import OwnerPermissionMixin

from .models import Client


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('clients:clients_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, OwnerPermissionMixin, generic.UpdateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('clients:clients_list')
    login_url = reverse_lazy('users:login')


class ClientDeleteView(LoginRequiredMixin, OwnerPermissionMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy('clients:clients_list')
    login_url = reverse_lazy('users:login')
