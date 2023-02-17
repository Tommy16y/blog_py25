from django.db import models
from applications.post.models import Post
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator,MaxValueValidator


User = get_user_model()
class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')
    is_like = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.owner} liked -{self.post.title}'


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ratings')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='ratings')
    rating = models.SmallIntegerField( validators=[MinValueValidator(1), MaxValueValidator(5)],blank=True,null=True)
    

    def __str__(self):
        return f'{self.owner} --> {self.post.title}'


class Favorite(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='favorites')
    post = models.ForeignKey( Post, on_delete=models.CASCADE,related_name='favorites')
