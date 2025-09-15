CREATE SCHEMA IF NOT EXISTS content;
CREATE EXTENSION "uuid-ossp";

#Таблица с фильмами
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE INDEX film_work_title_idx ON content.film_work(title);
CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);
#Предполагаю что запросы по rating будут обладать низкой селективностью, поэтому считаю не нужным индекс по этому столбцу


#Таблица с жанрами
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);
#Думаю что жанров будет не очень много (<5k), в индексе по name нет необходимости

#Таблица с людьми
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);
CREATE INDEX person_full_name_idx ON content.film_work(full_name);

#Промежуточная таблица люди-фильм
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
	person_id uuid NOT NULL REFERENCES content.person(id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
	role TEXT NOT NULL,
    created timestamp with time zone
);
CREATE UNIQUE INDEX person_film_work_idx ON content.person_film_work(film_work_id, person_id, role);
# Исключаем дубликаты в таблице, + добавляем скорости при поиске.


#Промежуточная таблица жанр-фильм
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id  uuid NOT NULL REFERENCES content.genre(id) ON DELETE CASCADE,
    film_work_id  uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    created timestamp with time zone
);
CREATE UNIQUE INDEX genre_film_work_idx ON content.genre_film_work(film_work_id, genre_id);
# Исключаем дубликаты в таблице, + добавляем скорости при поиске.


#Заполнение данными

