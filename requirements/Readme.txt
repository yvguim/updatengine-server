# Conf bdd sqlite
apt-get install libapache2-mod-wsgi python-virtualenv python-pip libxml2-dev libxslt-dev python-dev libsqlite3-dev

# Conf bdd mysql
#apt-get install libapache2-mod-wsgi python-virtualenv python-pip libxml2-dev libxslt-dev python-dev libmysqlclient-dev

cd /var/www/
virtualenv --no-site-packages UE-environment
cd /var/www/UE-environment/
sudo git clone https://github.com/updatengine/updatengine-server.git
/var/www/UE-environment/bin/pip install -r requirements/prod-sqlite.txt
#/var/www/UE-environment/bin/pip install -r requirements/prod-mysql.txt

chown -R www-data:www-data /var/www/UE-environment/UpdatEngine/UpdatEngine/db
/var/www/UE-environment/bin/python UpdatEngine/manage.py syncdb
/var/www/UE-environment/bin/ UpdatEngine/manage.py migrate

# Adapt settings.py with appropriate Url for your project
# Create apache conf file:
sudo cp apache-updatengine /etc/apache2/sites-available/
a2ensite apache-updatengine
service apache2 reload

# Create certificat

openssl genrsa -out updatengine.key 1024
openssl req -new -x509 -days 3650 -key updatengine.key -out updatengine.crt

cp updatengine.key /etc/ssl/private/
cp updatengine.crt /etc/ssl/certs/
a2enmod ssl

# help certificat
http://curl.haxx.se/docs/sslcerts.html
