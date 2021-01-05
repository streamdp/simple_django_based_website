sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/default  /etc/nginx/sites-enabled/
sudo /etc/init.d/nginx restart
sudo rm -rf /etc/gunicorn.d/test_conf.py
sudo rm -rf /etc/gunicorn.d/django_conf.py
sudo ln -sf /home/box/web/etc/gunicorn.conf   /etc/gunicorn.d/test_conf.py
sudo ln -sf /home/box/web/etc/django_conf.py /etc/gunicorn.d/django_conf.py
sudo mkdir -p /etc/mysql/mysql.conf.d/
sudo ln -sf /home/box/web/etc/django.cnf /etc/mysql/mysql.conf.d/
sudo /etc/init.d/gunicorn restart
sudo /etc/init.d/mysql start
/home/box/web/etc/setup_git.sh
