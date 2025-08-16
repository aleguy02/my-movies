# my movies

my movies is a simple web app I made for personal use to track movies that I wanted to watch. The app uses a microservice architecture for the frontend, backend, and redis database. Read compose.yaml for more information.

## Setup

If you are curious to learn more about how the backend and frontend work, they have their own READMEs that go into more detail. Here, I'll focus on leveraging Docker Compose to get you up and running as soon as possible. So, to start the application, do:

```bash
docker compose up -d
```

then go to localhost:3000 to view the app. That's it! It's super simple by design. If you want to stop the application, simply do:

```bash
docker compose down
```

## Usage

The main screen has two parts: a movie form and a list of movies you are currently tracking.

The movie form has two inputs: the movie name and a note. The movie name must be spelled correctly and maintain the punctuation of the actual title. It is case insensitive. The note is for you, and can be anything you want.
