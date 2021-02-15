from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass


#model for posts
class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    liked = models.BooleanField(default=False)
    total_likes = models.IntegerField(default=0)
    user_who_liked = models.ManyToManyField('User', blank=True, related_name="user_liked")

    class Meta:
        ordering = ('-created',)

    def serialize(self):
        return {
            "total_likes":self.total_likes
            }
    
    def __str__(self):
        return self.body

#model for likes #I haven't used it for this specification but may use it in the future.

class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True, related_name="post_liked")
    who_liked_it = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name="liker")


#model for followers
class Author(models.Model):
    user_from = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rel_from_set', blank=True, null=True)
    user_to = models.ForeignKey('User', related_name='rel_to_set', on_delete=models.CASCADE, blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'













