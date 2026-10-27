from django.urls import path

from . import views

urlpatterns = [
    path("directors/", views.DirectorListView.as_view()),
    path("directors/<int:pk>/", views.DirectorDetailView.as_view()),
    path("genres/", views.GenreListView.as_view()),
    path("genres/<int:pk>/", views.GenreDetailView.as_view()),
    path("movies/", views.MovieListView.as_view()),
    path("movies/<int:pk>/", views.MovieDetailView.as_view()),
]