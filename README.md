## Flask Docker API

This is a simple API made in Flask and *hopefully* deployed from a Docker container

### Important commands

Starting Flask app in debug mode for testing  
`flask --app api/app run --debug`  
Shortcut: `make flask-debug`

Running tests  
`pytest`

Starting redis instance for testing  
`docker start test-redis`

Stopping redis instance  
`docker stop test-redis`

