from flask import Flask, jsonify, request
import requests
from markupsafe import escape
from redis.exceptions import ResponseError

from api.redis_client import redis_connection

API_KEY = "3e4bbdc8"
app = Flask(__name__)
r = redis_connection()


@app.route("/")
def index():
    return "How to call this api:\nTODO: make docs"


## TODO: Handle duplicate post
@app.post("/api/movies")
def post_movie():
    """
    Adds movie to my list
    """
    note = request.form["note"]
    deconstructed_title = [
        word.strip().lower() for word in request.form["title"].split()
    ]
    title_for_url = "+".join(deconstructed_title)
    res = requests.post(
        "https://www.omdbapi.com/?", params={"t": title_for_url, "apiKey": API_KEY}
    )
    response_data = res.json()

    ## Error handling
    if response_data.get("Response") == "False":
        return jsonify({"Error": response_data.get("Error", "Unknown Error")}), 404

    scheme = {
        "_title": response_data.get("Title", request.form["title"]).strip(),
        "_genres": [s.strip().lower() for s in response_data.get("Genre").split(",")],
        "_note": note,
    }

    # write data to redis
    r.hset(
        scheme.get("_title").lower(),
        mapping={
            "title": scheme.get("_title"),
            "note": scheme.get("_note"),
        },
    )

    # delete anything that might be there
    r.delete(f"{scheme.get("_title").lower()}:genres")

    # and write movie genres
    r.rpush(f"{scheme.get("_title").lower()}:genres", *scheme.get("_genres"))

    return (
        jsonify(
            {
                "message": f"Movie added successfully!",
                "title": scheme.get("_title"),
                "genres": scheme.get("_genres"),
                "note": scheme.get("_note"),
            }
        ),
        201,
    )


@app.get("/api/movies")
def get_movies():
    try:
        out = {}
        for num, key in enumerate(r.keys("*")):
            if r.type(key) != "hash":
                continue

            out[key] = {
                "title": r.hget(key, "title"),
                "note": r.hget(key, "note"),
                "genres": r.lrange(f"{key}:genres", 0, -1),
            }

        return jsonify(out), 200
    except ResponseError as e:
        print(e)
        return "", 500


@app.delete("/api/movies")
def drop_movie():
    title = str(request.args.get("t")).strip().lower()
    removes = r.delete(title)
    r.delete(f"{title}:genres")

    return (
        ({"message": "Movie deleted successfully!", "title": title}, 202)
        if removes > 0
        else ({"message": "Movie not found"}, 200)
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
