from flask import Flask, jsonify, request
import requests
from markupsafe import escape

API_KEY = "3e4bbdc8"
app = Flask(__name__)

dummy_db = {}


@app.route("/")
def index():
    return "hello world"


@app.post("/api/movies")
def post_movie():
    """
    example schema:
        { title: string, note: string }
    """
    note = request.form["note"]
    deconstructed_title = [word for word in request.form["title"].split()]
    title_for_url = "+".join(deconstructed_title)
    r = requests.post(
        "https://www.omdbapi.com/?", params={"t": title_for_url, "apiKey": API_KEY}
    )
    response_data = r.json()

    ## Error handling
    if response_data.get("Response") == "False":
        return jsonify({"Error": response_data.get("Error", "Unknown Error")}), 404

    scheme = {
        "_title": response_data.get("Title", request.form["title"]),
        "_genres": [s.strip().lower() for s in response_data.get("Genre").split(",")],
        "_note": note,
    }
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
