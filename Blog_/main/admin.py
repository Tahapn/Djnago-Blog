from django.contrib import admin
from .models import Post
# Register your models here.


@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id','title','status']
    ordering = ['status','created_at']
    readonly_fields = ['profile']
    