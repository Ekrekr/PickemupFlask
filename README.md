# FlaskAPIRelay

Flask server for relaying API requests, for preventing having to share API key client side.

## Deployment

For a fresh Ubuntu 18.04 VM:

1. `ssh blog-server`

1. `git clone https://github.com/Ekrekr/BlogServer && cd BlogServer`

1. `sudo apt-get install docker`

1. `docker build -t blog .`

1. `docker run -d -p 5000:80 blog`

