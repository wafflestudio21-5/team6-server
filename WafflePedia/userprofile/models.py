from django.db import models
from waffleAuth.models import WaffleUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.

class Movie(models.Model):
    movieCD = models.CharField(max_length=20, primary_key=True)
    title_ko = models.CharField(max_length=100, null=False)
    title_original = models.CharField(max_length=100)
    plot = models.TextField()
    runtime = models.IntegerField()
    prod_country = models.CharField(max_length=50)
    poster = models.URLField()
    release_date = models.DateField()
    cumulative_audience = models.IntegerField()
    screening = models.BooleanField()


# 랭킹은 뷰에서 따로 처리


class Rating(models.Model):
    rating = [(i/2,str(i/2)) for i in range(1,11)]
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(WaffleUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Comment(models.Model):
    created_by = models.ForeignKey(WaffleUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.OneToOneField(Rating, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation('Like')


class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(WaffleUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey()


class State(models.Model):
    user = models.ForeignKey(WaffleUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    STATE_CHOICES = [
        ("want_to_watch", "Want to Watch"),
        ("watching", "Watching"),
        ("not_interested", "Not Interested")
    ]
    state = models.CharField(max_length=15, choices=STATE_CHOICES)

    class Meta:
        unique_together = ('user', 'movie')