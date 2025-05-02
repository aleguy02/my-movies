import requests

endpoint = "http://127.0.0.1:5000/api/movies"


class TestPost:
    def test_create_movie(self):
        """
        Test adding a movie with a note
        """
        response = requests.post(
            endpoint, data={"title": "inglourious basterds", "note": "Hellstorm knew"}
        )

        assert response.status_code == 201
        assert response.json()["title"] == "Inglourious Basterds"
        assert response.json()["genres"] == ["adventure", "drama", "war"]
        assert response.json()["note"] == "Hellstorm knew"

    def test_invalid_title(self):
        """
        Test unable to add a movie with an invalid title
        """
        response = requests.post(endpoint, data={"title": "bad title", "note": ""})

        assert response.status_code == 404


if __name__ == "__main__":
    ## Debugging
    pass
