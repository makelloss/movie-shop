from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import Conflict
from .models import Director, Genre, Movie
from .serializers import DirectorSerializer, GenreSerializer, MovieSerializer


class BaseListView(APIView):
    """GET — список, POST — створення."""

    model = None
    serializer_class = None

    def get(self, request):
        objects = self.model.objects.all()
        serializer = self.serializer_class(objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BaseDetailView(APIView):
    """GET — один об'єкт, PUT/PATCH — редагування, DELETE — видалення."""

    model = None
    serializer_class = None
    object_name = "Об'єкт"

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(f"{self.object_name} з id={pk} не знайдено.")

    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(self.serializer_class(obj).data)

    def put(self, request, pk):
        return self.update(request, pk, partial=False)

    def patch(self, request, pk):
        return self.update(request, pk, partial=True)

    def update(self, request, pk, partial):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        self.check_can_delete(obj)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def check_can_delete(self, obj):
        """Перевизначається там, де є обмеження на видалення."""


class DirectorListView(BaseListView):
    model = Director
    serializer_class = DirectorSerializer


class DirectorDetailView(BaseDetailView):
    model = Director
    serializer_class = DirectorSerializer
    object_name = "Режисера"

    def check_can_delete(self, obj):
        count = obj.movies.count()
        if count:
            raise Conflict(
                f"Неможливо видалити режисера «{obj.name}», оскільки за ним "
                f"закріплено фільмів: {count}. Спочатку видаліть ці фільми "
                f"або змініть у них режисера."
            )


class GenreListView(BaseListView):
    model = Genre
    serializer_class = GenreSerializer


class GenreDetailView(BaseDetailView):
    model = Genre
    serializer_class = GenreSerializer
    object_name = "Жанр"

    def check_can_delete(self, obj):
        count = obj.movies.count()
        if count:
            raise Conflict(
                f"Неможливо видалити жанр «{obj.name}», оскільки до нього "
                f"належать фільми: {count}. Спочатку видаліть ці фільми "
                f"або змініть у них жанр."
            )


class MovieListView(BaseListView):
    model = Movie
    serializer_class = MovieSerializer


class MovieDetailView(BaseDetailView):
    model = Movie
    serializer_class = MovieSerializer
    object_name = "Фільм"