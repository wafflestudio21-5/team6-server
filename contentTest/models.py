from django.db import models


class Movie(models.Model):
    movieCd = models.CharField(max_length=20, primary_key=True, db_column='movieCD')
    movieNm = models.CharField(max_length=100, null=False, db_column='title_ko')
    movieNmEn = models.CharField(max_length=100, db_column='title_original') # 사실 원어명이 아니라 영어명임
    # runtime = models.IntegerField()
    nationAlt = models.CharField(max_length=50, db_column='prod_country')
    # poster = models.URLField()
    openDt = models.DateField(db_column='release_date')
    # cumulative_audience = models.IntegerField()
    # screening = models.BooleanField()
