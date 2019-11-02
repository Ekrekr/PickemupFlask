# Install Linux packages.
sudo apt-get update && sudo apt-get upgrade
sudo apt-get -y install python3 python3-venv nginx git build-essential python3-dev gcc

# Configure nginx for forwarding to flask server.
rm /etc/nginx/sites-enabled/default
mkdir /var/www/blog/
cp blog_nginx.conf /var/www/blog/
sudo ln -s /var/www/blog/blog_nginx.conf /etc/nginx/conf.d/

# Configure uWSGI
cp blog_uwsgi.ini /var/www/blog/
sudo mkdir -p /var/log/uwsgi
sudo chown -R ubuntu:ubuntu /var/log/uwsgi

# Install python modules.
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt

