from rest_framework import serializers

from .models import Director, Genre, Movie


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(source="movies.count", read_only=True)

    class Meta:
        model = Director
        fields = ["id", "name", "birth_year", "movies_count"]


class GenreSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(source="movies.count", read_only=True)

    class Meta:
        model = Genre
        fields = ["id", "name", "movies_count"]


class MovieSerializer(serializers.ModelSerializer):
    director_name = serializers.CharField(source="director.name", read_only=True)
    genre_name = serializers.CharField(source="genre.name", read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id", "title", "year", "description", "price",
            "director", "director_name", "genre", "genre_name",
        ]