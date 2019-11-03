# FlaskAPIRelay

Flask server for relaying API requests, for preventing having to share API key client side.

## Deployment

For a fresh Ubuntu 18.04 VM. First navigate to parent directory of `.keys` which contains private API keys that are gitignored.

1. `scp -r .keys azblog:~/.keys`

1. `ssh azblog`

1. `git clone https://github.com/Ekrekr/BlogServer && cd BlogServer && mv .keys BlogServer/app/`

1. `screen -r sudo docker-compose up`

1. `ctrl-a` `ctrl-d` to dislocate.

1. `screen -r` to resume.

## Notes

* Docker image from [tiangolo](https://github.com/tiangolo/uwsgi-nginx-flask-docker/tree/master/python3.7).

