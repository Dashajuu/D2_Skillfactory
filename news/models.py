from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    userAuth = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingUser = models.IntegerField(default=0)

    # суммарный рейтинг каждой статьи автора умножается на 3;
    # суммарный рейтинг всех комментариев автора;
    # суммарный рейтинг всех комментариев к статьям автора;
    def update_rating(self):
        post = self.post_set.aggregate(sum_ratingPost=Sum("ratingPost"))
        comAuth = self.userAuth.comment_set.aggregate(sum_ratingCom=Sum("ratingCom"))
        comPost = Comment.objects.filter(post__author=self).aggregate(sum_PostCom=Sum("ratingCom"))

        self.ratingUser = ((post['sum_ratingPost']*3 or 0) + (comAuth['sum_ratingCom'] or 0) + (comPost['sum_PostCom'] or 0))
        self.save()


class Category(models.Model):
    subject = models.CharField(max_length=65, unique=True)

    def __str__(self):
        return self.subject


class Post(models.Model):
    articlePost = 'A'
    newsPost = 'N'

    TYPES = [
        (articlePost, 'Статья'),
        (newsPost, 'Новость')
    ]

    typePost = models.CharField(max_length=2, choices=TYPES, default=newsPost)
    dataPost = models.DateTimeField(auto_now_add=True)
    namePost = models.CharField(max_length=255)
    textPost = models.TextField()
    ratingPost = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.ratingPost += 1
        self.save()

    def dislike(self):
        self.ratingPost -= 1
        self.save()

    def preview(self):
        return self.textPost[:124] + '...'

    def __str__(self):
        return f"{self.namePost}: {self.preview()}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post - {self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    textCom = models.TextField(max_length=2000)
    dateCom = models.DateTimeField(auto_now_add=True)
    ratingCom = models.IntegerField(default=0)

    def like(self):
        self.ratingCom += 1
        self.save()

    def dislike(self):
        self.ratingCom -= 1
        self.save()

    def get_rat(self):
        return self.ratingCom


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
