from django.db import models


class Movie(models.Model):
    movieCd = models.CharField(max_length=20, primary_key=True) # KOBIS LIST, KOBIS DETAIL
    movieNm = models.CharField(max_length=100, null=False) # KOBIS LIST, KOBIS DETAIL
    movieNmOg = models.CharField(max_length=100, null=True) # KOBIS DETAIL
    plot = models.TextField(null=True) # KMDB
    showTm = models.IntegerField(null=True)  # KOBIS DETAIL
    nationAlt = models.CharField(max_length=50, null=True) # KOBIS LIST, KOBIS DETAIL
    poster = models.URLField(null=True) #KMDB
    openDt = models.DateField(db_column='release_date', null=True) # KOBIS LIST
    # cumulative_audience = models.IntegerField()
    # screening = models.BooleanField()
