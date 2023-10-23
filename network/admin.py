from django.contrib import admin
from django.contrib import admin
from .models import User, PostModel, LikeModel, CommentModel

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'profile_picture')  
    filter_horizontal = ('followers', 'following')


class PostModelAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_at')  

class LikeModelAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'post', 'user',)

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text', 'created_at')  

admin.site.register(User, CustomUserAdmin)
admin.site.register(PostModel, PostModelAdmin)
admin.site.register(LikeModel, LikeModelAdmin)
admin.site.register(CommentModel, CommentModelAdmin)

