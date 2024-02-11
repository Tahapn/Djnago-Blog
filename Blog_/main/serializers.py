from rest_framework.serializers import ModelSerializer
from main.models import Post, Comment, Like , Profile , BlogImage
from rest_framework import serializers


class ProfileBlosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title']
class ProfileLikeSerializer(serializers.ModelSerializer):
    blog = ProfileBlosSerializer() 
    class Meta:
        model = Like
        fields = ['id','blog','datetime']

class ProfileSerializer(ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    likes = ProfileLikeSerializer(many=True,source = 'like_set')
    class Meta:
        model = Profile
        fields = ['id','date_joined','birth_date','likes']


class ImageBlogSerializer(ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id','image','title']

    def create(self, validated_data):
        blog_id = self.context['blog_id']
        return BlogImage.objects.create(blog_id = blog_id, ** validated_data)


class BlogSerializer(ModelSerializer):

    images = ImageBlogSerializer(many=True)

    profile_id = serializers.IntegerField(read_only = True)
    likes_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = Post
        fields = ['id','title','text','profile_id','images','last_modified','likes_count']


class MyBlogSeriliazer(serializers.ModelSerializer):
    images = ImageBlogSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ['id','title','text','images']

    def create(self, validated_data):
        profile_id = self.context['profile_id']
        return Post.objects.create(profile=profile_id , **validated_data)


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','text','date','blog_id']

    def create(self, validated_data):
        blog_id = self.context['blog_id']
        profile_id = self.context['profile_id']
        print(profile_id)
        return Comment.objects.create(profile_id = profile_id , blog_id = blog_id, **validated_data)
    

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['blog_id','profile_id']




