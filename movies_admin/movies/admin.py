from django.contrib import admin
from .models import Genre, FilmWork, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "id")


class PersonFilmWorkInline(admin.TabularInline):
    autocomplete_fields = ('person',)
    model = PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "get_genres"
    )
    list_prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()][:2])
        # Тут я добавил [:2] на случай, если у фильма будет куча жанров, во избежания каши и многобукв
    get_genres.short_description = 'Жанры фильма'

    search_fields = ("title", "description", "id")
    list_filter = ("type",)
