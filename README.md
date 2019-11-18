# Pickemup Flask

Flask server for Pickemup. Given a **solution request**, retrieves the corresponding [Distance Matrix](https://developers.google.com/maps/documentation/distance-matrix/start), and uses [Google OR-Tools](https://developers.google.com/optimization/routing) to efficiently solve the travelling salesman problem.

## Deployment

For a fresh Ubuntu 18.04 VM. First navigate to parent directory of `.keys`, which contains the private API keys that are gitignored.

Assuming your `~/.ssh/config` has the VM set as `pflask`, then the exact commands are:

1. `scp -r .keys pflask:~/.keys`

1. `ssh pflask`

1. `sudo apt-get update && sudo apt-get install docker docker-compose`

1. `git clone https://github.com/Ekrekr/PickemupFlask && mv .keys PickemupFlask/pickemup/ && cd PickemupFlask`

1. `sudo docker-compose up -d`

To check the server is visible, open the i.p. address of `pflask` in a browser.

### Reattaching

1. `sudo docker container ls` to view the container `<id>`

1. `sudo docker attach <id>` to attach to it. Note that no output will be shown so it may appear frozen.

### Viewing logs

1. `sudo docker logs <id>`

### Stopping and Removing

1. `sudo docker container stop <id>`

1. `sudo docker container rm <id>`

## Running Tests

From the base directory, run `pytest -s`.

## Notes

* Docker image from [tiangolo](https://github.com/tiangolo/uwsgi-nginx-flask-docker).

* Example [flask project with pytest](https://github.com/aaronjolson/flask-pytest-example/blob/master/tests/test_routes.py).
