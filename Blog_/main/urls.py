from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from main.views import BlogImageViewSet, BlogViewSet, CommentViewSet, MyBlogViewSet, MyProfile , LikeToggleView , Test
from django.urls import include,path


router = routers.SimpleRouter()

router.register('myblogs',viewset=MyBlogViewSet,basename='myblogs')

router.register('blogs',viewset=BlogViewSet)
comment_router = routers.NestedSimpleRouter(router,'blogs',lookup ='blog')
comment_router.register('comments',CommentViewSet,basename='blog-comments')

image_router = routers.NestedSimpleRouter(router,'myblogs',lookup='myblog')
image_router.register('images',viewset= BlogImageViewSet,basename='myblog-images')

urlpatterns = [
    path('myprofile',MyProfile.as_view()),
    path('blogs/<int:blog_pk>/like/', LikeToggleView.as_view()),
] + router.urls + comment_router.urls + image_router.urls