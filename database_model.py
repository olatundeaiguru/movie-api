from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Movie(Base):


    __tablename__ = "Movie"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    director = Column(String)
    genre = Column(String)
    rating = Column(Float)
    release_year = Column(Integer)
