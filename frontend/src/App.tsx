import { useState, useEffect } from 'react';

interface MovieType {
  title: string;
  note: string;
  genres: Array<string>;
}

function App() {
  const [movies, setMovies] = useState<MovieType[]>([]);
  const [title, setTitle] = useState('');
  const [note, setNote] = useState('');
  const [refresh, setRefresh] = useState(0);

  // Fetch movies when the component is mounted
  // TODO: occurs twice on mount, look into unsubscribe func?
  useEffect(() => {
    fetch('http://localhost:8000/api/movies')
      .then((response) => response.json())
      .then((data) => {
        const out: MovieType[] = [];
        for (const [key, value] of Object.entries(data)) {
          out.push(value as MovieType);
        }
        console.log(out);
        setMovies(out);
        console.log('done');
      })
      .catch((error) => console.error('Error fetching movies:', error));
  }, [refresh]);

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // set up data to adhere to content-type: multipart/form-data
    const formData = new FormData();
    formData.append('title', title);
    formData.append('note', note);

    // make request
    fetch('http://localhost:8000/api/movies', {
      method: 'POST',
      body: formData,
    })
      .then(() => {
        setRefresh((prev) => prev + 1);
        console.log('submit success');
      })
      .catch((error) => console.error('Error submitting movie:', error));

    setTitle('');
    setNote('');
  };

  // Handle deleting a movie
  const handleDelete = (movieTitle: string) => {
    // The backend expects the title as a query parameter "t", lowercased and trimmed
    fetch(
      `http://localhost:8000/api/movies?t=${encodeURIComponent(
        movieTitle.trim().toLowerCase()
      )}`,
      {
        method: 'DELETE',
      }
    )
      .then(() => {
        setRefresh((prev) => prev + 1);
      })
      .catch((error) => console.error('Error deleting movie:', error));
  };

  return (
    <div>
      <h1>Movies and Shows</h1>
      <ul>
        {movies.map((movie, index) => (
          <li
            key={index}
            style={{ cursor: 'pointer', transition: 'opacity 0.2s' }}
            title="Click to delete"
            onClick={() => handleDelete(movie.title)}
            onMouseEnter={(e) => (e.currentTarget.style.opacity = '0.7')}
            onMouseLeave={(e) => (e.currentTarget.style.opacity = '1')}
          >
            <strong>{movie.title}</strong>: {movie.genres.join(', ')} |{' '}
            {movie.note}
          </li>
        ))}
      </ul>

      {/* Form to add a new movie */}
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Title:
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </label>
        </div>
        <div>
          <label>
            Note:
            <input
              type="text"
              value={note}
              onChange={(e) => setNote(e.target.value)}
              required
            />
          </label>
        </div>
        <button type="submit">Add Movie</button>
      </form>
    </div>
  );
}

export default App;
