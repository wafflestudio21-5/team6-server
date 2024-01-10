from django.db import models
from waffleAuth.models import WaffleUser


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

    def __str__(self):
        return self.title_ko


class Genre(models.Model):
    genre = models.CharField(max_length=50)
    movies = models.ManyToManyField(
        Movie, related_name="genres"
    )

    def __str__(self):
        return self.genre


class Rating(models.Model):
    RATING_CHOICES = [(i / 2, str(i / 2)) for i in range(1, 11)]
    rate = models.DecimalField(choices=RATING_CHOICES, max_digits=3, decimal_places=1, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(WaffleUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.created_by.nickname + " - " + self.movie.title_ko


class People(models.Model):
    peopleCD = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    is_actor = models.BooleanField()
    is_director = models.BooleanField()
    is_writer = models.BooleanField()
    directed_movies = models.ManyToManyField(
        Movie, related_name="directors", blank=True
    )
    written_movies = models.ManyToManyField(
        Movie, related_name="writers", blank=True
    )
    starred_movies = models.ManyToManyField(
        Movie, related_name="casts", blank=True
    )

    def __str__(self):
        return self.name


class Role(models.Model):
    role = models.CharField(max_length=50)
    actor = models.ForeignKey(People, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie.title_ko + " - " + self.actor.name + " - " + self.role


class State(models.Model):
    user = models.ForeignKey(WaffleUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    STATE_CHOICES = [
        ("want_to_watch", "want_to_watch"),
        ("watching", "watching"),
        ("not_interested", "not_interested")
    ]
    user_state = models.CharField(choices=STATE_CHOICES, max_length=20, blank=True)

    def __str__(self):
        return self.movie.title_ko + " - " + self.user.nickname
