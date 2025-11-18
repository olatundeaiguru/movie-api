from fastapi import FastAPI, Depends
from database_connection import session, engine
from sqlalchemy.orm import Session
from pydantic_model import Movie
import database_model


app = FastAPI()

database_model.Base.metadata.create_all(bind=engine)

movies = [
    Movie(
        id=1,
        title="Anikulapo",
        director="Kunle Afolayan",
        genre="Tradition",
        rating=8.6,
        release_year=23,
    ),
    Movie(
        id=2,
        title="Anikulapo",
        director="Kunle Afolayan",
        genre="Tradition",
        rating=8.6,
        release_year=23,
    ),
    Movie(
        id=3,
        title="Anikulapo",
        director="Kunle Afolayan",
        genre="Tradition",
        rating=8.6,
        release_year=23,
    )
]

def get_db():

    db = session()
    try:
        yield db
    finally:
        db.close()
        

def init_db():
    db = session()
    count = db.query(database_model.Movie).count()
    
    if count == 0: 
        for movie in movies:
            db.add(database_model.Movie(**movie.model_dump()))
        db.commit()
    print("Data loaded Succesfully") 
    return "Data added succesfully"
    
init_db()


def init_db():
    pass


@app.get("/movie")
def get_all_movies(db: Session = Depends(get_db)):
    db_movie = db.query(database_model.Movie).all()
    return db_movie

@app.get("/movie/{id}")
def get_movie_by_id(id: int, db: Session = Depends(get_db)):
    db_movie = db.query(database_model.Movie).filter(database_model.Movie.id == id).first()
    
    if db_movie:
        return db_movie
    else:
        return "Movie notfound"

@app.put("/movie")
def add_movie(movie:Movie, db: Session = Depends(get_db)):
    db.add(database_model.Movie(**movie.model_dump()))
    db.commit()
    return movie

@app.put("/movie/{id}")
def update_movie(id: int, movie: Movie, db: Session = Depends(get_db)):
    db_movie = db.query(database_model.Movie).filter(database_model.Movie.id == id).first()
    
    if db_movie:
        db_movie.title = movie.title
        db_movie.director = movie.director
        db_movie.genre = movie.genre
        db_movie.rating = movie.rating
        db_movie.release_year = movie.release_year
        db.commit()
        return db_movie
    else:
        return "movie not found"
    
@app.delete("/movie/{id}")
def delete_movie(id: int, db: Session = Depends(get_db)):
    db_movie = db.query(database_model.Movie).filter(database_model.Movie.id == id).first()
    if db_movie:
        db.delete(db_movie)
        db.commit()
        return "Movie deleted successful"
    return "No Movie found"