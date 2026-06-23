# MovieHub — Movie Recommendation System (Django)

A full-stack movie recommendation website built entirely with Django and
plain Python — no JavaScript frameworks, no external CSS frameworks, no
third-party ML libraries. Recommendations are generated with a simple
genre-matching algorithm written from scratch.

## Features

- Browse a catalog of 41 well-known movies across 10 languages (English,
  Hindi, Telugu, Tamil, Malayalam, Kannada, Korean, Japanese, Spanish, French)
- Search by title/director, filter by genre and language, sort by rating /
  year / title
- User accounts (sign up, log in, log out) using Django's built-in auth
- Rate movies 1–5 stars; ratings can be updated
- Personal watchlist (add/remove)
- "Recommended For You" page: a content-based recommendation engine that
  looks at the genres of movies you rated 4★ or 5★ and suggests other
  movies that share those genres (see `movies/recommender.py` — it's
  plain Python, fully commented, no external libraries)
- "You might also like" section on every movie's detail page
- Django admin panel for managing movies, genres, and ratings

## Tech stack

- Python 3 + Django (backend, templating, ORM, auth — everything)
- SQLite (default Django database, zero setup)
- Plain HTML templates (Django Template Language) + one hand-written CSS
  file — no Bootstrap, no Tailwind, no JS frameworks

## Project structure

```
moviehub/
├── manage.py
├── requirements.txt
├── moviehub/              # project settings, urls
├── movies/                # the app: models, views, forms, admin
│   ├── models.py          # Genre, Movie, Rating, Watchlist
│   ├── recommender.py     # the recommendation algorithm
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── management/commands/populate_movies.py   # seeds 41 sample movies
├── templates/              # all HTML templates
└── static/css/style.css    # all styling
```

## Setup instructions

1. **Install Python 3.10+** if you don't already have it.

2. **Create a virtual environment (recommended) and install Django:**
   ```bash
   cd moviehub
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run migrations to create the database:**
   ```bash
   python manage.py migrate
   ```

4. **Load the sample movie data (41 movies, 12 genres):**
   ```bash
   python manage.py populate_movies
   ```

5. **Create an admin account (optional, lets you add/edit movies via /admin/):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. Open **http://127.0.0.1:8000/** in your browser.

## How the recommendation algorithm works

It's plain Python, no scikit-learn or pandas involved:

1. Find the movies the logged-in user rated 4★ or 5★.
2. Build a "taste profile" by counting how often each genre appears
   across those highly-rated movies.
3. Score every movie the user hasn't rated yet by adding up the taste
   profile points for its genres.
4. Sort by that score (ties broken by the movie's average rating from
   all users) and return the top results.

If a user hasn't rated anything yet, they just see the highest-rated
movies overall. The full implementation with comments is in
`movies/recommender.py`.

## Notes for presenting this project

- All movie data (titles, directors, years, descriptions) is seeded via
  `populate_movies.py` — open that file to add, remove, or edit movies.
- The `average_rating()` and `rating_count()` methods on the `Movie`
  model are computed live from the `Rating` table, not cached, which
  keeps the data model simple for a project this size.
- To reset the database at any point: delete `db.sqlite3`, then repeat
  steps 3–5 above.
