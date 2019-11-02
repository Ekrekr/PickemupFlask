# FlaskAPIRelay

Flask server for relaying API requests, for preventing having to share API key client side.

## Deployment

For a fresh Ubuntu 18.04 VM:

1. `ssh blog-server`

1. `git clone https://github.com/Ekrekr/BlogServer && cd BlogServer`

1. `chmod a+x setup.sh && sudo ./setup.sh`

1. `sudo /etc/init.d/nginx restart`

1. `source venv/bin/activate`

1. `screen`

1. `chmod a+x run.sh && run.sh`, then ctrl-a ctrl-d to swap back to main screen.

### Redeployment

1. `screen -r` to resume the screen session.

1. `./run.sh`, then ctrl-a ctrl-d.

