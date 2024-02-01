from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet ,ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly 
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import generics ,status ,filters , pagination
from django_filters.rest_framework import DjangoFilterBackend 
from django.db.models import Count
from main.serializers import BlogSerializer, CommentSerializer, ProfileSerializer , LikeSerializer , MyBlogSeriliazer ,ImageBlogSerializer
from main.models import Post, BlogImage, Comment , Profile , Like

# Create your views here.


class BlogViewSet(ReadOnlyModelViewSet):
    
    queryset = Post.objects.prefetch_related('images',).filter(status = 'PU').annotate(likes_count=Count('likes'))
    serializer_class = BlogSerializer

    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    filterset_fields = ['profile']
    ordering_fields = ['id','last_modified']
    search_fields = ['title']

    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 10
    pagination_class.page_size_query_param = 'page_size'


class MyBlogViewSet(ModelViewSet):
    
    def get_queryset(self):
        profile = Profile.objects.only('id').get(user= self.request.user.id)
        
        return Post.objects.prefetch_related('images').filter(profile = profile) 

    serializer_class = MyBlogSeriliazer
    permission_classes = [IsAuthenticated]


    def get_serializer_context(self):
        profile_id = Profile.objects.only('id').get(user= self.request.user.id)

        return {'profile_id':profile_id}



class MyProfile(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        prorfile = Profile.objects.get(user = self.request.user.id)
        serializer = ProfileSerializer(prorfile)
        return Response(serializer.data)
    
    def patch(self,request):
        profile = Profile.objects.get(user = self.request.user.id)
        serializer = ProfileSerializer(profile,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(blog_id = self.kwargs['blog_pk'])
    

    def get_serializer_context(self):
        return {'blog_id': self.kwargs['blog_pk']}

    
class LikeToggleView(generics.CreateAPIView):

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request,*args,**kwargs):
        
        # Check if the user has already liked the blog
        blog_id = self.kwargs['blog_pk']
        profile = Profile.objects.get(user_id = self.request.user.id)
        like_exists = Like.objects.filter(profile = profile, blog_id=blog_id).exists()

        if like_exists:
            # User has already liked, unlike it
            Like.objects.filter(profile = profile, blog_id=blog_id).delete()
            return Response({'message': 'Blog unliked successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            # User hasn't liked, create a new like
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(profile = profile, blog_id=blog_id)
            return Response({'message': 'Blog liked successfully'}, status=status.HTTP_201_CREATED)
        

class BlogImageViewSet(ModelViewSet):
    
    def get_queryset(self):
        return BlogImage.objects.filter(blog_id = self.kwargs['myblog_pk'])
    serializer_class = ImageBlogSerializer

    def get_serializer_context(self):
        return {'blog_id': self.kwargs['myblog_pk']}

