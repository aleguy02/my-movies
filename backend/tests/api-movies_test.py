import requests

endpoint = "http://127.0.0.1:5000/api/movies"


class TestPost:
    def test_create_movie(self):
        """
        Test adding a movie with a note
        """
        response = requests.post(
            endpoint, data={"title": "inglourious basterds", "note": "Hellstrom knew"}
        )

        assert response.status_code == 201
        assert response.json()["title"] == "Inglourious Basterds"
        assert response.json()["genres"] == ["adventure", "drama", "war"]
        assert response.json()["note"] == "Hellstrom knew"
        # assert that redis instance was updated with this info

    def test_format_request(self):
        """
        Test adding a movie with a note
        """
        response = requests.post(
            endpoint,
            data={"title": "IngLouRious    Basterds", "note": "Hellstrom knew"},
        )

        assert response.status_code == 201
        assert response.json()["title"] == "Inglourious Basterds"
        assert response.json()["genres"] == ["adventure", "drama", "war"]
        assert response.json()["note"] == "Hellstrom knew"
        # assert that redis instance was updated with this info

    def test_invalid_title(self):
        """
        Test unable to add a movie with an invalid title
        """
        response = requests.post(endpoint, data={"title": "bad title", "note": ""})

        assert response.status_code == 404
        # assert that redis instance was NOT updated with this info


if __name__ == "__main__":
    ## Debugging
    pass
