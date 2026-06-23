from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:pk>/watchlist-toggle/', views.toggle_watchlist, name='toggle_watchlist'),
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('signup/', views.signup, name='signup'),
]
