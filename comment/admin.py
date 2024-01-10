from django.contrib import admin
from .models import Comment, Reply, Like

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like)
