from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Movie, Genre, Rating, Watchlist, LANGUAGE_CHOICES
from .forms import SignUpForm, RatingForm
from .recommender import get_recommendations_for_user, similar_movies


def home(request):
    """Landing page: shows a small recommended row (personalized if logged
    in, otherwise just newest movies) plus the full catalog below."""
    recommended = get_recommendations_for_user(request.user, limit=6)
    latest_movies = Movie.objects.all()[:8]
    context = {
        'recommended': recommended,
        'latest_movies': latest_movies,
    }
    return render(request, 'movies/home.html', context)


def movie_list(request):
    movies = Movie.objects.all().prefetch_related('genres')

    query = request.GET.get('q', '').strip()
    genre_id = request.GET.get('genre', '')
    language = request.GET.get('language', '')
    sort = request.GET.get('sort', 'newest')

    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(director__icontains=query))
    if genre_id:
        movies = movies.filter(genres__id=genre_id)
    if language:
        movies = movies.filter(language=language)

    movies = movies.distinct()

    if sort == 'rating':
        movies = sorted(movies, key=lambda m: m.average_rating(), reverse=True)
    elif sort == 'year':
        movies = sorted(movies, key=lambda m: m.release_year, reverse=True)
    elif sort == 'title':
        movies = sorted(movies, key=lambda m: m.title)
    # 'newest' is already the default model ordering

    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'genres': Genre.objects.all(),
        'languages': LANGUAGE_CHOICES,
        'query': query,
        'selected_genre': genre_id,
        'selected_language': language,
        'sort': sort,
    }
    return render(request, 'movies/movie_list.html', context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie.objects.prefetch_related('genres', 'ratings'), pk=pk)
    user_rating = None
    in_watchlist = False

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, movie=movie).first()
        in_watchlist = Watchlist.objects.filter(user=request.user, movie=movie).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.movie = movie
            rating.save()
            messages.success(request, f'Your rating for "{movie.title}" was saved.')
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = RatingForm(instance=user_rating)

    context = {
        'movie': movie,
        'form': form,
        'user_rating': user_rating,
        'in_watchlist': in_watchlist,
        'similar': similar_movies(movie),
    }
    return render(request, 'movies/movie_detail.html', context)


@login_required
def toggle_watchlist(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    item, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        item.delete()
        messages.info(request, f'Removed "{movie.title}" from your watchlist.')
    else:
        messages.success(request, f'Added "{movie.title}" to your watchlist.')
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('movie_detail', pk=movie.pk)


@login_required
def watchlist_view(request):
    items = Watchlist.objects.filter(user=request.user).select_related('movie')
    return render(request, 'movies/watchlist.html', {'items': items})


@login_required
def recommendations_view(request):
    recommended = get_recommendations_for_user(request.user, limit=12)
    has_ratings = Rating.objects.filter(user=request.user).exists()
    return render(request, 'movies/recommendations.html', {
        'recommended': recommended,
        'has_ratings': has_ratings,
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to MovieHub, {user.username}!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
