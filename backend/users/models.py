from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='user'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='author'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
