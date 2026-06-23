"""
Simple content-based recommendation engine.

How it works (in plain terms):
1. Look at the movies the logged-in user rated 4 or 5 stars.
2. Collect the genres of those movies into a "taste profile" -
   a genre gets points equal to how many times it shows up in
   the user's highly-rated movies.
3. Go through every movie the user HASN'T rated yet and score it
   by adding up the taste-profile points for each genre it has.
4. Sort movies by that score (highest first), then by average
   rating from all users as a tie-breaker.

This is a basic form of content-based filtering. It doesn't need
any external ML library - just counting and sorting - which keeps
it easy to explain and easy to extend later (e.g. weighting by
language preference, release year, etc.)
"""
from collections import Counter
from .models import Movie, Rating


def get_recommendations_for_user(user, limit=8):
    if not user.is_authenticated:
        return Movie.objects.order_by('-added_on')[:limit]

    liked_ratings = Rating.objects.filter(user=user, score__gte=4).select_related('movie')
    liked_movie_ids = [r.movie_id for r in liked_ratings]

    rated_movie_ids = Rating.objects.filter(user=user).values_list('movie_id', flat=True)

    if not liked_movie_ids:
        # New user / no high ratings yet -> just show the highest rated movies
        # that they haven't already rated.
        candidates = Movie.objects.exclude(id__in=rated_movie_ids)
        return sorted(candidates, key=lambda m: m.average_rating(), reverse=True)[:limit]

    # Step 1: build taste profile (genre -> weight)
    taste_profile = Counter()
    liked_movies = Movie.objects.filter(id__in=liked_movie_ids).prefetch_related('genres')
    for movie in liked_movies:
        for genre in movie.genres.all():
            taste_profile[genre.id] += 1

    # Step 2: score every unrated movie
    candidates = Movie.objects.exclude(id__in=rated_movie_ids).prefetch_related('genres')
    scored = []
    for movie in candidates:
        genre_score = sum(taste_profile.get(g.id, 0) for g in movie.genres.all())
        if genre_score > 0:
            scored.append((genre_score, movie.average_rating(), movie))

    # Step 3: sort by genre match first, then by average rating
    scored.sort(key=lambda tup: (tup[0], tup[1]), reverse=True)

    recommendations = [movie for _, _, movie in scored[:limit]]

    # Fallback: if not enough genre matches, top up with highly rated movies
    if len(recommendations) < limit:
        existing_ids = {m.id for m in recommendations}
        backfill = Movie.objects.exclude(id__in=rated_movie_ids).exclude(id__in=existing_ids)
        backfill = sorted(backfill, key=lambda m: m.average_rating(), reverse=True)
        recommendations += backfill[: limit - len(recommendations)]

    return recommendations


def similar_movies(movie, limit=6):
    """Find movies that share genres with the given movie - used on the
    movie detail page as "You might also like"."""
    genre_ids = movie.genres.values_list('id', flat=True)
    candidates = Movie.objects.filter(genres__id__in=genre_ids).exclude(id=movie.id).distinct()
    scored = []
    for m in candidates:
        overlap = m.genres.filter(id__in=genre_ids).count()
        scored.append((overlap, m.average_rating(), m))
    scored.sort(key=lambda tup: (tup[0], tup[1]), reverse=True)
    return [m for _, _, m in scored[:limit]]
