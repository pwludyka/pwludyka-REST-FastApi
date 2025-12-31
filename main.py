from fastapi import FastAPI
from fastapi import HTTPException
import requests
import sqlite3
from typing import Any

app = FastAPI()



### Basic Calculations

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/sum")
def sum(x: int = 0, y: int = 10):
    return x+y

@app.get("/subtract")
def subtract(x: int = 0, y: int = 10):
    return x-y

@app.get("/multiply")
def multiply(x: int = 0, y: int = 10):
    return x*y

@app.get("/geocode")
def geocode(lat: float, lon: float):
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
    Location = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return Location.json()

### DB duplications - refactored

def get_db():
    db = sqlite3.connect("movies-extended.db")
    return db

def fetch_one(query, params=()):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    
def fetch_all(query, params=()):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
def execute_write(query, params=()):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(query, params)
        db.commit()
        return cursor.rowcount, cursor.lastrowid
        

### Movies

@app.get("/movies")
def get_movies():
    output = []
    movies = fetch_all("SELECT * FROM movie")
    for movie in movies:
        movie = {"ID": movie[0], "title": movie[1], "director": movie[2], "year": movie[3], "description": movie[4]}
        output.append(movie)
    return output

@app.get("/movies/{movie_id}")
def get_single_movie(movie_id: int):
    movie = fetch_one("SELECT * FROM movie WHERE id=?", (movie_id,))
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Movie with id={movie_id} not found")
    return {"ID": movie[0], "title": movie[1], "director": movie[2], "year": movie[3], "description": movie[4]}

@app.post("/movies")
def add_movie(params: dict[str, Any]):
    title = params.get("title")
    director = params.get("director")
    year = params.get("year")
    description = params.get("description")
    if not title or not director or year is None or not description:
        raise HTTPException(status_code = 400, detail="Fields required: title, director, year, description")
    row_count, new_id = execute_write("INSERT INTO movie (title, director, year, description) VALUES(?, ?, ?, ?)", (title, director, year, description))
    return {"message": "Movie added successfully", "id": new_id}

@app.delete("/movies/{movie_id}")
def delete_single_movie(movie_id: int):
    row_count, new_id = execute_write("DELETE FROM movie WHERE id=?", (movie_id,))
    if row_count == 0:
        raise HTTPException(status_code = 404, detail=f"Movie with id={movie_id} not found")
    return {"message": f"Movie id={movie_id} successfully deleted"}

@app.put("/movies/{movie_id}")
def update_one_movie(movie_id:int, params: dict[str, Any]):
    movies_cols = ["title", "director", "year", "description"]
    cols = []
    values = []
    for key in params:
        if key in movies_cols:
            cols.append(f"{key} = ?")
            values.append(params[key])
    if len(cols) == 0:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    values.append(movie_id)
    query = f"""UPDATE movie SET {", ".join(cols)} WHERE id = ? """
    row_count, new_id = execute_write(query, tuple(values))
    if row_count == 0:
        raise HTTPException(status_code = 404, detail=f"Movie with id={movie_id} not found")
    return {"message": "Movie updated successfully", "id": movie_id, "updated fields": list(params.keys())}
    
@app.delete("/movies")
def delete_all_movies():
    row_count, new_id = execute_write("DELETE from movie")
    return {"message": f"Movies database erased. {row_count} movies deleted"}


### Actors

@app.get("/actors")
def get_actors():
    output = []
    actors = fetch_all("SELECT * FROM actor")
    for actor in actors:
        actor = {"ID": actor[0], "name": actor[1], "surname": actor[2]}
        output.append(actor)
    return output

@app.get("/actors/{actor_id}")
def get_single_actor(actor_id: int):
    actor = fetch_one("SELECT * FROM actor WHERE id=?", (actor_id,))
    if actor is None:
        raise HTTPException(status_code=404, detail=f"Actor with id={actor_id} not found")
    return {"ID": actor[0], "name": actor[1], "surname": actor[2]}

@app.delete("/actors/{actor_id}")
def delete_single_actor(actor_id: int):
    row_count, new_id = execute_write("DELETE FROM actor WHERE id=?", (actor_id,))
    if row_count == 0:
        raise HTTPException(status_code = 404, detail=f"Actor with id={actor_id} not found")
    return {"message": f"Actor id={actor_id} successfully deleted"}

@app.delete("/actors")
def delete_all_actors():
    row_count, new_id = execute_write("DELETE from actor")
    return {"message": f"Actors database erased. {row_count} actors deleted"}

@app.post("/actors")
def add_actor(params: dict[str, Any]):
    name = params.get("name")
    surname = params.get("surname")
    if not name or not surname:
        raise HTTPException(status_code = 400, detail="Fields required: name, surname")
    row_count, new_id = execute_write("INSERT INTO actor (name, surname) VALUES(?, ?)", (name, surname))
    return {"message": "Actor added successfully", "id": new_id}

@app.put("/actors/{actor_id}")
def update_one_actor(actor_id:int, params: dict[str, Any]):
    actors_cols = ["name", "surname"]
    cols = []
    values = []
    for key in params:
        if key in actors_cols:
            cols.append(f"{key} = ?")
            values.append(params[key])
    if len(cols) == 0:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    values.append(actor_id)
    query = f"""UPDATE actor SET {", ".join(cols)} WHERE id = ? """
    row_count, new_id = execute_write(query, tuple(values))
    if row_count == 0:
        raise HTTPException(status_code = 404, detail=f"Actor with id={actor_id} not found")
    return {"message": "Actor updated successfully", "id": actor_id, "updated fields": list(params.keys())}


### MAP

@app.get("/map")
def get_map():
    output = []
    map = fetch_all("SELECT * FROM movie_actor_through")
    for link in map:
        link = {"ID": link[0], "movie_id": link[1], "actor_id": link[2]}
        output.append(link)
    return output

@app.get("/map/{map_id}")
def get_movie_actor_link(map_id: int):
    link = fetch_one("SELECT * FROM movie_actor_through WHERE id=?", (map_id,))
    if link is None:
        raise HTTPException(status_code=404, detail=f"Link with id={map_id} not found")
    return {"ID": link[0], "movie_id": link[1], "actor_id": link[2]}

@app.delete("/map/{map_id}")
def delete_actor_movie_link(map_id: int):
    row_count, new_id = execute_write("DELETE FROM movie_actor_through WHERE id=?", (map_id,))
    if row_count == 0:
        raise HTTPException(status_code = 404, detail=f"Link with id={map_id} not found")
    return {"message": f"Link id={map_id} successfully deleted"}

@app.delete("/map")
def delete_all_actor_movie_links():
    row_count, new_id = execute_write("DELETE from movie_actor_through")
    return {"message": f"Links database erased. {row_count} links deleted"}

@app.post("/map")
def add_movie_actor_link(params: dict[str, Any]):
    movie_id = params.get("movie_id")
    actor_id = params.get("actor_id")
    if movie_id is None or actor_id is None:
        raise HTTPException(status_code = 400, detail="Fields required: movie_id, actor_id")
    row_count, new_id = execute_write("INSERT INTO movie_actor_through (movie_id, actor_id) VALUES(?, ?)", (movie_id, actor_id))
    return {"message": "Link added successfully", "id": new_id}

@app.put("/map/{map_id}")
def update_one_movie_actor_link(map_id:int, params: dict[str, Any]):
    map_cols = ["movie_id", "actor_id"]
    cols = []
    values = []
    for key in params:
        if key in map_cols:
            cols.append(f"{key} = ?")
            values.append(params[key])
    if len(cols) == 0:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    values.append(map_id)
    query = f"""UPDATE movie_actor_through SET {", ".join(cols)} WHERE id = ? """
    row_count, new_id = execute_write(query, tuple(values))
    if row_count == 0:
        raise HTTPException(status_code = 404, detail=f"Link with id={map_id} not found")
    return {"message": "Link updated successfully", "id": map_id, "updated fields": list(params.keys())}


### Cast - Actors for Movies

@app.get("/movies/{movie_id}/cast")
def get_movie_cast(movie_id: int):
    rows = fetch_all("SELECT m.title, a.id, a.name, a.surname FROM movie m LEFT JOIN movie_actor_through mat ON mat.movie_id = m.id LEFT JOIN actor a ON a.id = mat.actor_id WHERE m.id=?", (movie_id,))
    if not rows:
        raise HTTPException(status_code=404, detail=f"Movie with id={movie_id} not found")
    cast = [{"id": r[1], "name": r[2], "surname": r[3]} for r in rows if r[1] is not None]
    title = rows[0][0]
    return {"ID": movie_id, "title": title, "cast": cast}