from django.db.models.query import QuerySet
from django.views import generic
from django.urls import reverse_lazy

from .models import Client
# Create your views here.


class ClientListView(generic.ListView):
    model = Client

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)


class ClientDetailView(generic.DetailView):
    model = Client


class ClientCreateView(generic.CreateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('clients:clients_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(generic.UpdateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('clients:clients_list')


class ClientDeleteView(generic.DeleteView):
    model = Client
    success_url = reverse_lazy('clients:clients_list')
