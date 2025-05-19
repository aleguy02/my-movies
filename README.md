# Flask Docker API

This is a simple API I made so I could keep track of movies I wanted to watch. It leverages the Open Movie Database API to get movies.

## Setup
Clone the repository into your machine. Move into the directory where you cloned it to and do the following command.  
```bash
docker compose up
```
And that's it! The app is now running across two containers: one for the app logic and one for a Redis data store. You can leave the app running or, when you're done using it, take it down with  
```bash
docker compose down
```
Don't worry, there's a volume set up to persist data. See `compose.yaml` and `Dockerfile` for more info.

## How to Use

### `POST /api/movies`

#### Description

Adds a movie to your list.

#### Request

* **Content-Type**: `application/x-www-form-urlencoded`
* **Body Parameters**:

  | Key   | Type   | Required | Description            |
  | ----- | ------ | -------- | ---------------------- |
  | title | string | ✅        | Title of the movie     |
  | note  | string | ✅        | Personal note about it |

#### Example Request

```http
POST /api/movies
Content-Type: application/x-www-form-urlencoded

title=The Matrix&note=A great sci-fi film
```

#### Example Success Response

```json
{
  "message": "Movie added successfully!",
  "title": "The Matrix",
  "genres": ["action", "sci-fi"],
  "note": "A great sci-fi film"
}
```

#### Example Error Response

```json
{
  "Error": "Movie not found!"
}
```

Status Code: `404`

### `GET /api/movies`

#### Description

Retrieves all saved movies, including title, note, and genres.

#### Request

```http
GET /api/movies
```

#### Example Success Response

```json
{
  "the matrix": {
    "title": "The Matrix",
    "note": "A great sci-fi film",
    "genres": ["action", "sci-fi"]
  },
  "toy story": {
    "title": "Toy Story",
    "note": "Childhood favorite",
    "genres": ["animation", "adventure", "comedy"]
  }
}
```

#### Error Responses

* `500 Internal Server Error`: Redis or unknown server error.

### `DELETE /api/movies`

#### Description

Deletes a movie entry and its genres by title.

#### Request

* **Query Parameters**:

  | Key | Type   | Required | Description                                     |
  | --- | ------ | -------- | ----------------------------------------------- |
  | t   | string | ✅        | Title of the movie to delete (case-insensitive) |

#### Example Request

```http
DELETE /api/movies?t=The Matrix
```

#### Example Success Response

```json
{
  "message": "Movie deleted successfully!",
  "title": "the matrix"
}
```

#### If Movie Not Found

```json
{
  "message": "Movie not found"
}
```

## Other commands

Starting Flask app in debug mode for testing  
`flask --app api/app run --debug`  
Shortcut: `make flask-debug`

Running tests  
`pytest`

Starting redis instance for testing  
`docker start test-redis`

Stopping redis instance  
`docker stop test-redis`
