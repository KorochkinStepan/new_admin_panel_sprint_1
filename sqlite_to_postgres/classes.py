import uuid
from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class FilmWork:
    id: uuid.UUID
    title: str
    creation_date: datetime.date
    file_path: str
    description: str
    rating: float
    type: str
    created_at: datetime.date
    updated_at: datetime.date

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)
        if isinstance(self.created_at, str):
            self.created_at = parse_datetime(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = parse_datetime(self.updated_at)


@dataclass
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime.date
    updated_at: datetime.date

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)
        if isinstance(self.created_at, str):
            self.created_at = parse_datetime(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = parse_datetime(self.updated_at)


@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    created_at: datetime.date
    updated_at: datetime.date

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)
        if isinstance(self.created_at, str):
            self.created_at = parse_datetime(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = parse_datetime(self.updated_at)


@dataclass
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime.date

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)
        if isinstance(self.film_work_id, str):
            self.film_work_id = uuid.UUID(self.film_work_id)
        if isinstance(self.genre_id, str):
            self.genre_id = uuid.UUID(self.genre_id)
        if isinstance(self.created_at, str):
            self.created_at = parse_datetime(self.created_at)


@dataclass
class PersonFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime.date

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)
        if isinstance(self.film_work_id, str):
            self.film_work_id = uuid.UUID(self.film_work_id)
        if isinstance(self.person_id, str):
            self.person_id = uuid.UUID(self.person_id)
        if isinstance(self.created_at, str):
            self.created_at = parse_datetime(self.created_at)


def parse_datetime(dt_str):
    """
    Функция для правильного парса времени (при вытягивании дат из SQLite и Postgres,
    в питоне оказываются по-разному представленные даты, приводим к одному формату)
    :param dt_str:
    :return:
    """
    if "+" in dt_str:
        dt_str = dt_str.split("+")[0]
    if "." in dt_str:  # Если микросекунды
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
    else:  # Если нет
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

    return dt.replace(tzinfo=ZoneInfo("Etc/UTC"))
