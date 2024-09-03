from django.shortcuts import render

from apps.clients.models import Client
from apps.mailing.models import Mailing
from apps.posts.models import Post


def index(request):
    mailings_total = Mailing.objects.all().count()
    active_mailings = Mailing.objects.filter(sending_task__enabled=True).count()
    unique_clients = Client.objects.distinct('email').count()
    posts = Post.objects.order_by('?')[:3]
    for post in posts:
        post.views_count += 1
        post.save()
    return render(request, 'main/index.html', {
        'mailings_total': mailings_total,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'posts': posts
    })
