from django.db import models
from django.conf import settings
# Create your models here.


class Profile(models.Model):
    date_joined = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    birth_date = models.DateField(null = True)

    def __str__(self) -> str:
        return  self.user.username 


class Post(models.Model):
    pending = 'PE'
    published = 'PU'

    BLOG_STATUS = [
        (pending,'Pending'),
        (published, 'Published')
    ]

    title = models.CharField(max_length=255)
    text = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length= 2,choices=BLOG_STATUS,default = pending)
    profile = models.ForeignKey(Profile,on_delete=models.PROTECT,)

    def __str__(self) -> str:
        return f'{self.pk}  {self.title}'


class BlogImage(models.Model):
    image = models.ImageField(upload_to='images')
    title = models.CharField(max_length = 55)
    blog = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = 'images')

    def __str__(self) -> str:
        return self.title


class Like(models.Model):
    blog = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = 'likes')
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField(max_length=555)
    date = models.DateTimeField(auto_now=True,)
    blog = models.ForeignKey(Post,on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete = models.PROTECT)