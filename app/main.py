from flask import Flask, request
from pydantic import ValidationError
from sqlalchemy.dialects.postgresql import insert as postgres_upsert

import app.models as models
from app.db import Session, Movies
from app.config import Settings

settings = Settings()

app = Flask("movie_review")
app.config["ENV"] = settings.ENV


@app.get("/v1/movies")
def get_movies():
    with Session.begin() as session:
        movies = [
            models.Movie.from_orm(item).dict() for item in session.query(Movies).all()
        ]

    return movies


@app.post("/v1/movies")
def post_movies():
    data = request.get_json(force=True, silent=True)

    if not data:
        return {"message": "Error parsing body"}, 422

    try:
        data = models.Movies(items=data)
    except ValidationError as e:
        # get first elem from the errors
        error = e.errors()[0]
        e_loc = error["loc"][0]
        e_msg = error["msg"]

        return {"message": f"Error in field '{e_loc}'. Detail: {e_msg}"}, 422

    with Session.begin() as session:
        stmt = postgres_upsert(Movies).values([item.dict() for item in data.items])

        stmt = stmt.on_conflict_do_update(
            index_elements=[Movies.year],
            set_=dict(
                vote_average=stmt.excluded.vote_average, quantity=stmt.excluded.quantity
            ),
        )
        session.execute(stmt)

    return f"{data}"


if __name__ == "__main__":
    app.run()
