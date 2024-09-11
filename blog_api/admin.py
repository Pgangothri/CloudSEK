from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('user_id','title', 'text', 'created_at')
    search_fields = ('title', 'text')
    list_filter = ('created_at',)