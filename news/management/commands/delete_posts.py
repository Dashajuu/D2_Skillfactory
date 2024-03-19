from django.core.management.base import BaseCommand, CommandError
from news.models import Post


class Command(BaseCommand):
    help = 'Delete posts of choosen category'
    missing_args_message = 'Недостаточно аргументов: введите id категории'

    def add_arguments(self, parser):
        parser.add_argument('argument', nargs=1, type=int)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Do you really want to delete all posts in category? yes/no')
        answer = input()
        cat_id = options['argument'][0]

        if answer == 'yes':
            Post.objects.filter(category=cat_id).delete()
            self.stdout.write(self.style.SUCCESS('Done!'))
            return

        self.stdout.write(self.style.ERROR('No!'))