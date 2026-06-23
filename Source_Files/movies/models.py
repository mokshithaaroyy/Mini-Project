from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


LANGUAGE_CHOICES = [
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('Telugu', 'Telugu'),
    ('Tamil', 'Tamil'),
    ('Malayalam', 'Malayalam'),
    ('Kannada', 'Kannada'),
    ('Korean', 'Korean'),
    ('Japanese', 'Japanese'),
    ('Spanish', 'Spanish'),
    ('French', 'French'),
]


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='movies')
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    release_year = models.PositiveIntegerField()
    director = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    poster_url = models.URLField(blank=True, help_text="Link to a poster image (optional)")
    duration_minutes = models.PositiveIntegerField(default=120)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-release_year', 'title']

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    def get_absolute_url(self):
        return reverse('movie_detail', args=[self.id])

    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return round(sum(r.score for r in ratings) / ratings.count(), 1)

    def rating_count(self):
        return self.ratings.count()


class Rating(models.Model):
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title}: {self.score}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist_items')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='in_watchlists')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_on']

    def __str__(self):
        return f"{self.user.username} -> {self.movie.title}"
