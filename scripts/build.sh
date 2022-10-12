#!/usr/bin/env bash
: '
COPYRIGHT 2022 MONTA

This file is part of Monta.

Monta is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Monta is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Monta.  If not, see <https://www.gnu.org/licenses/>.
---------------------------------------------------------------------

This script is used to build the project from scratch.
It is used to set up the project on a new machine.
'

echo 'Starting up...'

# Install dependencies
echo 'Installing dependencies...'
apt-get update
apt-get install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx git curl redis-server libssl-dev libffi-dev build-essential python3-venv
pip3 install --upgrade pip
pip3 install virtualenv

# Install Redis
echo 'Installing Redis...'
apt-get install -y build-essential tcl
cd /tmp || exit
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable || exit
make
make test
make install
cd utils || exit
./install_server.sh
cd ~ || exit
rm -rf /tmp/redis-stable
rm /tmp/redis-stable.tar.gz

# Create database
echo 'Creating database...'
sudo -u postgres psql -c "CREATE DATABASE monta;"
sudo -u postgres psql -c "CREATE USER monta WITH PASSWORD 'monta';"
sudo -u postgres psql -c "ALTER ROLE monta SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE monta SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE monta SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE monta TO monta;"
sudo -u postgres psql -c "ALTER USER monta CREATEDB;"
sudo -u postgres psql -c "ALTER USER monta SUPERUSER;"
sudo -u postgres psql -c "ALTER USER monta WITH PASSWORD 'monta';"

# Create virtual environment
echo 'Creating virtual environment...'
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt

# Create database tables
echo 'Creating database tables...'
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser
echo 'Creating superuser...'
python3 manage.py createsuperuser --username monta --email

# Create nginx config
echo 'Creating nginx config...'
echo "server {
    listen 80;
    server_name monta.com;

    location /static/ {
        alias /home/ubuntu/monta/static/;
    }

    location / {
        proxy_pass http://
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}" > /etc/nginx/sites-available/monta
ln -s /etc/nginx/sites-available/monta /etc/nginx/sites-enabled
rm /etc/nginx/sites-enabled/default
service nginx restart

# Create gunicorn service
echo 'Creating gunicorn service...'
echo "[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/monta
ExecStart=/home/ubuntu/monta/venv/bin/gunicorn --workers 3 --bind unix:monta.sock monta.wsgi:application

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/monta.service
systemctl start monta
systemctl enable monta

# Create celery service
echo 'Creating celery service...'
echo "[Unit]
Description=celery worker daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/monta
ExecStart=/home/ubuntu/monta/venv/bin/celery -A monta worker -l info

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/celery.service
systemctl start celery
systemctl enable celery

# Create celery beat service
echo 'Creating celery beat service...'
echo "[Unit]
Description=celery beat daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/monta
ExecStart=/home/ubuntu/monta/venv/bin/celery -A monta beat -l info

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/celerybeat.service
systemctl start celerybeat
systemctl enable celerybeat

# Create celery flower service
echo 'Creating celery flower service...'
echo "[Unit]
Description=celery flower daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/monta
ExecStart=/home/ubuntu/monta/venv/bin/celery -A monta flower

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/celeryflower.service
systemctl start celeryflower
systemctl enable celeryflower

# Create Redis service
echo 'Creating Redis service...'
echo "[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
ExecStop=/usr/local/bin/redis-cli shutdown

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/redis.service
systemctl start redis
systemctl enable redis

# Create Redis sentinel service
echo 'Creating Redis sentinel service...'
echo "[Unit]
Description=Redis Sentinel
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-sentinel /etc/redis/sentinel.conf --sentinel

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/redis-sentinel.service
systemctl start redis-sentinel
systemctl enable redis-sentinel

# Create Redis cluster service
echo 'Creating Redis cluster service...'
echo "[Unit]
Description=Redis Cluster
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis-cluster.conf --cluster-enabled yes --appendonly yes

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/redis-cluster.service
systemctl start redis-cluster
systemctl enable redis-cluster

# Run tests
echo 'Running tests...'
python3 manage.py test

# Collect static files
echo 'Collecting static files...'
python3 manage.py collectstatic

# Restart services
echo 'Restarting services...'
systemctl restart monta
systemctl restart celery
systemctl restart celerybeat
systemctl restart celeryflower
systemctl restart redis
systemctl restart redis-sentinel
systemctl restart redis-cluster

# Create swap file
echo 'Creating swap file...'
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# Install and configure fail2ban
echo 'Installing and configuring fail2ban...'
apt-get install -y fail2ban
echo "[DEFAULT]
ignoreip =
bantime = 3600
findtime = 600
maxretry = 3
backend = auto
destemail = [email protected]
sendername = Fail2Ban
mta = sendmail
banaction = iptables-multiport
action_ = %(action_mwl)s
action_mwl = %(action_)s[name=%(__name__)s, port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]
actionstart =
actionstop =
actioncheck =

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 5
bantime = 3600
findtime = 600
backend = auto
" > /etc/fail2ban/jail.local
systemctl restart fail2ban

# Install and configure ufw
echo 'Installing and configuring ufw...'
apt-get install -y ufw
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 6379
ufw allow 26379
ufw allow 7000

# Install and configure certbot
echo 'Installing and configuring certbot...'
apt-get install -y software-properties-common
add-apt-repository ppa:certbot/certbot
apt-get update
apt-get install -y certbot python-certbot-nginx

# Install and configure monit
echo 'Installing and configuring monit...'
apt-get install -y monit
echo "set daemon 60
set logfile /var/log/monit.log
set mailserver localhost
set alert [email protected]
set eventqueue
    basedir /var/lib/monit/events
    slots 100

check process nginx with pidfile /var/run/nginx.pid
    start program = "/etc/init.d/nginx start"
    stop program = "/etc/init.d/nginx stop"
    if failed host

check process monta with pidfile /var/run/monta.pid
    start program = "/etc/init.d/monta start"
    stop program = "/etc/init.d/monta stop"
    if failed host

check process celery with pidfile /var/run/celery.pid
    start program = "/etc/init.d/celery start"
    stop program = "/etc/init.d/celery stop"
    if failed host

check process celerybeat with pidfile /var/run/celerybeat.pid
    start program = "/etc/init.d/celerybeat start"
    stop program = "/etc/init.d/celerybeat stop"
    if failed host

check process celeryflower with pidfile /var/run/celeryflower.pid
    start program = "/etc/init.d/celeryflower start"
    stop program = "/etc/init.d/celeryflower stop"
    if failed host

check process redis with pidfile /var/run/redis.pid
    start program = "/etc/init.d/redis start"
    stop program = "/etc/init.d/redis stop"
    if failed host

check process redis-sentinel with pidfile /var/run/redis-sentinel.pid
    start program = "/etc/init.d/redis-sentinel start"
    stop program = "/etc/init.d/redis-sentinel stop"
    if failed host

check process redis-cluster with pidfile /var/run/redis-cluster.pid
    start program = "/etc/init.d/redis-cluster start"
    stop program = "/etc/init.d/redis-cluster stop"
    if failed host

check process fail2ban with pidfile /var/run/fail2ban/fail2ban.pid
    start program = "/etc/init.d/fail2ban start"
    stop program = "/etc/init.d/fail2ban stop"
    if failed host

check process ufw with pidfile /var/run/ufw.pid
    start program = "/etc/init.d/ufw start"
    stop program = "/etc/init.d/ufw stop"
    if failed host

check process certbot with pidfile /var/run/certbot.pid
    start program = "/etc/init.d/certbot start"
    stop program = "/etc/init.d/certbot stop"
    if failed host

check process monit with pidfile /var/run/monit.pid
    start program = "/etc/init.d/monit start"
    stop program = "/etc/init.d/monit stop"
    if failed host

check system monta
    if loadavg (1min) > 4 then alert
    if loadavg (5min) > 2 then alert
    if memory usage > 80% then alert
    if cpu usage (user) > 80% then alert
    if cpu usage (system) > 80% then alert
    if cpu usage (wait) > 80% then alert
    if cpu usage (idle) < 20% then alert
    if cpu usage (total) > 80% then alert
    if cpu usage (guest) > 80% then alert
    if cpu usage (steal) > 80% then alert
    if cpu usage (nice) > 80% then alert
    if cpu usage (softirq) > 80% then alert
    if cpu usage (irq) > 80% then alert
    if cpu usage (iowait) > 80% then alert
    if cpu usage (user) > 80% for 5 cycles then alert
    if cpu usage (system) > 80% for 5 cycles then alert
    if cpu usage (wait) > 80% for 5 cycles then alert
    if cpu usage (idle) < 20% for 5 cycles then alert
    if cpu usage (total) > 80% for 5 cycles then alert
    if cpu usage (guest) > 80% for 5 cycles then alert
    if cpu usage (steal) > 80% for 5 cycles then alert
    if cpu usage (nice) > 80% for 5 cycles then alert
    if cpu usage (softirq) > 80% for 5 cycles then alert
    if cpu usage (irq) > 80% for 5 cycles then alert
    if cpu usage (iowait) > 80% for 5 cycles then alert
    if memory usage > 80% for 5 cycles then alert
    if failed port 80 protocol http request "/health" then alert
    if failed port 443 protocol http request "/health" then alert
    if failed port 6379 protocol http request "/health" then alert
    if failed port 26379 protocol http request "/health" then alert
    if failed port 7000 protocol http request "/health" then alert
    if failed port 80 protocol
    " > /etc/monit/monitrc
systemctl restart monit