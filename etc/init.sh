sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -sf $PWD/default  /etc/nginx/sites-enabled/
sudo /etc/init.d/nginx restart
sudo mkdir -p /etc/gunicorn.d/
sudo rm -rf /etc/gunicorn.d/test_conf.py
sudo rm -rf /etc/gunicorn.d/django_conf.py
sudo ln -sf $PWD/gunicorn.conf   /etc/gunicorn.d/test_conf.py
sudo ln -sf $PWD/django_conf.py /etc/gunicorn.d/django_conf.py
sudo mkdir -p /etc/mysql/mysql.conf.d/
sudo ln -sf $PWD/django.cnf /etc/mysql/mysql.conf.d/
sudo /etc/init.d/gunicorn restart
sudo /etc/init.d/mysql start
$PWD/setup_git.sh
