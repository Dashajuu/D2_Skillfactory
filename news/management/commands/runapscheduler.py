import logging

from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from django.contrib.auth.models import User
from news.models import Post, Category

logger = logging.getLogger(__name__)


def my_job():
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
        to=subscriber
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', hour='18', minute='00'),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")