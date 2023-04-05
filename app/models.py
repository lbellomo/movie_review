from pydantic import BaseModel


class Movie(BaseModel):
    year: int
    vote_average: float
    quantity: int

    class Config:
        orm_mode = True


class Movies(BaseModel):
    items: list[Movie]

    class Config:
        orm_mode = True
