from django.views import generic
from django.urls import reverse_lazy

from apps.mailing.models import Message
# Create your views here.


class MessageListView(generic.ListView):
    model = Message
    template_name = 'mailing/message/message_list.html'
    
    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageDetailView(generic.DetailView):
    model = Message
    template_name = 'mailing/message/message_detail.html'


class MessageCreateView(generic.CreateView):
    model = Message
    template_name = 'mailing/message/message_form.html'
    fields = ('title', 'body')
    success_url = reverse_lazy('mailing:messages_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(generic.UpdateView):
    model = Message
    template_name = 'mailing/message/message_form.html'
    fields = ('title', 'body')
    success_url = reverse_lazy('mailing:messages_list')


class MessageDeleteView(generic.DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages_list')
