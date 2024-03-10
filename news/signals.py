from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.models import User
from .models import Post
from .tasks import notify_new_post


@receiver(post_save, sender=Post)
def post_added(instance, **kwargs):
    notify_new_post.delay(instance.pk)

# @receiver(m2m_changed, sender=PostCategory)
# def post_added(instance, action, **kwargs):
    # if action == 'post_add':
    #     emails = User.objects.filter(
    #         subscriptions__category__in=instance.category.all()
    #     ).values_list('email', flat=True)
    #
    #     subject = f'Новый пост в категории {instance.category.all().values_list("subject", flat=True)[0]}'
    #
    #     text_content = (
    #         f'{instance.namePost}\n\n'
    #         f'{instance.preview()}\n'
    #         f'Прочитать полностью можно по ссылке: http://127.0.0.1:8000{instance.get_absolute_url()}'
    #     )
    #
    #     html_content = (
    #         f'<b>{instance.namePost}</b><br><br>'
    #         f'{instance.preview()}<br>'
    #         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
    #         f'Прочитать полностью</a>'
    #     )
    #
    #     for email in emails:
    #         msg = EmailMultiAlternatives(subject, text_content, None, [email])
    #         msg.attach_alternative(html_content, 'text/html')
    #         msg.send()
