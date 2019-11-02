# FlaskAPIRelay

Flask server for relaying API requests, for preventing having to share API key client side.

## Deployment

For a fresh Ubuntu 18.04 VM:

1. `ssh blog-server`

1. `git clone https://github.com/Ekrekr/BlogServer`

1. `sudo apt-get update && sudo apt-get upgrade`

1. `sudo apt-get -y install python3 python3-venv`

1. `cd BlogServer`

1. `python3 -m venv env`

1. `source env/bin/python3`

1. `python3 -m pip install -r requirements.txt`

1. `chmod a+x run.sh`

1. `screen -r ./run.sh`

To update requirements use `python3 -m pip freeze > requirements.txt`.

To redeploy the server use:

1. `./run.sh`

