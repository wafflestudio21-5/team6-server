from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from waffleAuth.models import WaffleUser
from content.models import Movie, Rating


class Comment(models.Model):
    created_by = models.ForeignKey(WaffleUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.OneToOneField(Rating, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation('Like')

    def __str__(self):
        return self.movie.title_ko + " - " + self.content[:20]


class Reply(models.Model):
    created_by = models.ForeignKey(WaffleUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation('Like')

    def __str__(self):
        return str(self.comment.id) + " - " + self.content[:20]


class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(WaffleUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey()

    def __str__(self):
        return f"({self.created_by}, {self.liked_object})"
