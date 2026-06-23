from django.contrib import admin
from .models import Genre, Movie, Rating, Watchlist


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'release_year', 'average_rating', 'rating_count']
    list_filter = ['language', 'genres', 'release_year']
    search_fields = ['title', 'director']
    filter_horizontal = ['genres']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'score', 'created_on']
    list_filter = ['score']


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'added_on']
