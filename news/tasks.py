from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

from .models import Post, Category


@shared_task
def notify_new_post(post_id):
    post = Post.objects.get(pk=post_id)
    category = post.category.all()
    subscriber = User.objects.filter(
        subscriptions__category__in=category).values_list('email', flat=True)

    subject = f'Новый пост в категории {category.values_list("subject", flat=True)[0]}'
    text = (f'{post.namePost}\n\n'
            f'{post.preview()}\n'
            f'Прочитать полностью можно по ссылке: http://127.0.0.1:8000{post.get_absolute_url()}')

    html_content = (f'<b>{post.namePost}</b><br><br>'
                    f'{post.preview()}<br>'
                    f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
                    f'Прочитать полностью</a>')

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text,
        to=subscriber,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_notification():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(dataPost__gte=last_week)
    categories = set(posts.values_list('category', flat=True))
    category_subject = Category.objects.filter(subscriptions__category__in=categories).values_list('subject', flat=True)
    subscriber = set(User.objects.filter(subscriptions__category__in=categories).values_list('email', flat=True))

    subject = f'Новое за неделю в категории {" ".join([i for i in category_subject])}'

    html_content = render_to_string(
        'week_mail.html',
        {'posts': posts},
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriber,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
