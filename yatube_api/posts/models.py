from django.contrib.auth import get_user_model
from django.db import models

User: models.Model = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user',)
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='no_self_following',
            ),
            models.UniqueConstraint(
                fields=('user', 'following',),
                name='unique_user_following'
            ),
        ]


class Group(models.Model):
    title = models.CharField('Название группы', max_length=128,)
    slug = models.SlugField(max_length=128,)
    description = models.CharField(max_length=256, null=True, blank=True,)

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',)
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True,)
    group = models.ForeignKey(
        Group, null=True, blank=True, on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',)
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True,)

    def __str__(self) -> str:
        return f'{self.author}: {self.text}'
