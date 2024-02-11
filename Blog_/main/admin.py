from django.contrib import admin
from .models import Post , Comment , Profile
# Register your models here.


@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id','title','status','last_modified']
    ordering = ['status','created_at']
    readonly_fields = ['profile']
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','text','blog']
    readonly_fields = ['blog','profile']
    search_fields = ['text']
    ordering = ['blog']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user']
    readonly_fields = ['user']
    