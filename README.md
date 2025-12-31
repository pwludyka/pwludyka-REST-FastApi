# Lab 2 – REST API
Projekt zaliczeniowy – REST API zbudowane w FastAPI z bazą SQLite.

## Wymagania
pip install -r requirements.txt

## Uruchomienie
fastapi dev main.py

## API dostępne pod
http://127.0.0.1:8000

## Testowanie
GET - lista filmów
http://127.0.0.1:8000/movies

GET - jeden film
http://127.0.0.1:8000/movies/1

GET - lista aktorów
http://127.0.0.1:8000/actors

GET - jeden aktor
http://127.0.0.1:8000/actors/1

GET - lista relacji film-aktor
http://127.0.0.1:8000/map

GET - jedna relacja film-aktor
http://127.0.0.1:8000/map/1

GET - lista aktorów dla danego filmu
http://127.0.0.1:8000/movies/4/cast


## Testowanie-Swagger
http://127.0.0.1:8000/docs

POST - dodaj film
{
  "title": "Test Title",
  "director": "Test Director",
  "year": 2025,
  "description": "Description of the test movie"
}

PUT - zaktualizuj film
{
  "title": "Test Title",
  "director": "Test Director",
  "year": 2025,
  "description": "Description of the test movie"
}

DELETE - usuń film
  movie_id

DELETE - usuń wszystkie filmy
Execute

POST - dodaj aktora
{
  "name": "Test_Name",
  "surname": "Test_Surname"
}

PUT - zaktualizuj aktora
{
  "name": "Test_Name",
  "surname": "Test_Surname"
}

DELETE - usuń jednego aktora
  movie_id

DELETE - usuń wszystkich aktorów
Execute

POST - dodaj połączenie film-aktor
{
  "movie_id": "Test_Movie_ID",
  "actor_id": "Test_Actor_ID"
}

PUT - zaktualizuj jedno połączenie film-aktor
{
  "movie_id": "Test_Movie_ID",
  "actor_id": "Test_Actor_ID"
}

DELETE - usuń jedno połączenie film-aktor
  movie_id

DELETE - usuń wszystkie połączenia film-aktor
Execute
