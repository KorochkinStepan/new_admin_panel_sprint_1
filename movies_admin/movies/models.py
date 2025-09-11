from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.name

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


class Person(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.full_name

    full_name = models.CharField(_("full_name"), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class FilmWork(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.title

    MIN_LIMIT = MinValueValidator(limit_value=0)
    MAX_LIMIT = MaxValueValidator(limit_value=100)
    TYPE_CHOICES = [("movie", _("film")), ("tv_show", _("tv show"))]

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation_date"), blank=True, null=True)
    rating = models.FloatField(
        _("rating"), validators=[MIN_LIMIT, MAX_LIMIT], blank=True
    )
    type = models.CharField(_("type"), choices=TYPE_CHOICES)
    genres = models.ManyToManyField(Genre, through="GenreFilmWork")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Film Work")
        verbose_name_plural = _("Films")


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        "FilmWork", db_column="film_work_id", on_delete=models.CASCADE
    )
    genre = models.ForeignKey("Genre", db_column="genre_id", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    role = models.TextField(_("role"))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
