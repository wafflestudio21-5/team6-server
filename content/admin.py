from django.contrib import admin
from .models import *
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple


class GenreInline(admin.StackedInline):
    model = Genre.movies.through


class RoleInline(admin.StackedInline):
    model = Role


class DirectedMovieInline(admin.StackedInline):
    model = People.directed_movies.through


class WrittenMovieInline(admin.StackedInline):
    model = People.written_movies.through


class StarredMovieInline(admin.StackedInline):
    model = People.starred_movies.through


class PeopleInline(admin.StackedInline):
    model = People


class MovieAdmin(admin.ModelAdmin):
    inlines = [
        GenreInline,
        RoleInline
    ]
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }


class GenreAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }


class PeopleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }
    search_fields = ['name']


class CarouselAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(People, PeopleAdmin)
admin.site.register(Rating)
admin.site.register(Role)
admin.site.register(State)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(BoxOffice)
admin.site.register(BoxOfficeMovie)
