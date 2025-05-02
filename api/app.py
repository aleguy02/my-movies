from flask import Flask, jsonify, request
import requests
from markupsafe import escape

from api.redis_client import redis_connection

API_KEY = "3e4bbdc8"
app = Flask(__name__)
r = redis_connection()


@app.route("/")
def index():
    return "hello world"


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
        "_title": response_data.get("Title", request.form["title"]),
        "_genres": [s.strip().lower() for s in response_data.get("Genre").split(",")],
        "_note": note,
    }

    # write data to redis
    r.hset(
        scheme.get("_title"),
        mapping={
            "title": scheme.get("_title"),
            "note": scheme.get("_note"),
        },
    )
    r.delete(f"{scheme.get("_title")}:genres")
    # * is the spread operator in Python
    r.rpush(f"{scheme.get("_title")}:genres", *scheme.get("_genres"))

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
