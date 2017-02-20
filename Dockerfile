FROM ubuntu:14.04

RUN apt-get update && apt-get install --yes git-core postgresql-client libpq-dev python-psycopg2 python-dev \
    build-essential libjpeg-dev libssl-dev swig libffi-dev dbus libdbus-1-dev libdbus-glib-1-dev python-setuptools \
    redis-server apache2 git python-virtualenv libpq-dev python-psycopg2 \
    python-dev build-essential libjpeg-dev libssl-dev swig libffi-dev dbus libdbus-1-dev libdbus-glib-1-dev libapache2-mod-wsgi

WORKDIR /var/www

RUN git clone --recursive https://github.com/AltClick/pybossa-amnesty-microtasking.git
RUN easy_install pip

WORKDIR /var/www/pybossa-amnesty-microtasking

RUN ls -la
RUN pip install urllib3
RUN pip install -r requirements.txt

RUN sed "s|localhost/pybossa|postgres/pybossa|; \
         s|MONGO_HOST = 'localhost'|MONGO_HOST = 'mongo'|; \
         s|'localhost', 26379|'sentinel', 26379|;" settings_local.py.tmpl > settings_local.py

RUN sed 's|localhost/pybossa|postgres/pybossa|' alembic.ini.template > alembic.ini

RUN sed 's/<APP_DIR>/pybossa-amnesty-microtasking/' app.wsgi.tmpl > app.wsgi

COPY ./apache2.conf /etc/apache2/sites-available/decoders.amnesty.org.conf
RUN a2dissite 000-default.conf
RUN a2ensite decoders.amnesty.org.conf
RUN ln -sf /dev/stdout /var/log/apache2/access.log
RUN ln -sf /dev/stderr /var/log/apache2/error.log


EXPOSE 5000

COPY docker.sh docker.sh
RUN chmod +x docker.sh

CMD ["sh", "docker.sh"]
