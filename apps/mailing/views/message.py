from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from apps.main.permissions import OwnerPermissionMixin

from apps.mailing.models import Message


class MessageListView(LoginRequiredMixin, generic.ListView):
    model = Message
    template_name = 'mailing/message/message_list.html'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message
    template_name = 'mailing/message/message_form.html'
    fields = ('title', 'body')
    success_url = reverse_lazy('mailing:messages_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, OwnerPermissionMixin, generic.UpdateView):
    model = Message
    template_name = 'mailing/message/message_form.html'
    fields = ('title', 'body')
    success_url = reverse_lazy('mailing:messages_list')
    login_url = reverse_lazy('users:login')


class MessageDeleteView(LoginRequiredMixin, OwnerPermissionMixin, generic.DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages_list')
    login_url = reverse_lazy('users:login')
