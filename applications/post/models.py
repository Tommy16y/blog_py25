from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Post(models.Model):
    title = models.CharField('Название поста',max_length=50, null=True, blank=True)
    description = models.TextField('Описание поста')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts',verbose_name='Владалец поста')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    john = models.CharField(max_length=50, null=True,blank=True)
    
    # image = models.ImageField(upload_to='images',null=True,blank=True)

    def __str__(self):
        return f'{self.title}'
    
    def save(self):
        self.john = 'John'
        return super().save()
    


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.post.title}'
    
    


    

class Comment(models.Model):
    owner =  models.ForeignKey(User , on_delete=models.CASCADE, related_name='comments')
    post =  models.ForeignKey(Post , on_delete=models.CASCADE, related_name= 'comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} -> {self.post.title}'