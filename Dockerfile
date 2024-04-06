############################################################
# Dockerfile to build Flask App
# Based on
############################################################

# Set the base image
FROM debian:bullseye-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-pip \
    sqlite3 \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# Create directories and set permissions first
RUN mkdir -p /var/www/apache-flask/instance &&  \
    chown www-data:www-data /var/www/apache-flask/instance

# log directory : set permissions
RUN chown -R www-data:www-data /var/log/apache2/ && \
    chmod 755 -R /var/log/apache2/

# run directory : set permissions
RUN chown -R www-data:www-data /var/run/apache2/ && \
    chmod 755 -R /var/run/apache2/

# Copy over the wsgi file, run.py and the app
COPY  ./*.wsgi /var/www/apache-flask/
COPY  ./*.py /var/www/apache-flask/

# Set permissions for copied files
RUN chown -R www-data:www-data /var/www/apache-flask/ && \
    chmod 755 -R /var/www/apache-flask/

# Copy over and install the requirements
COPY ./app/requirements.txt /var/www/apache-flask/app/requirements.txt
RUN pip install -r /var/www/apache-flask/app/requirements.txt

COPY ./data/GolfServer.sql //var/www/apache-flask/data/GolfServer.sql
RUN sqlite3 /var/www/apache-flask/data/GolfServer.db < /var/www/apache-flask/data/GolfServer.sql

# Copy over the apache configuration file and enable the site
COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf

# Disable default site, enable custom site and enable required modules
RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf
RUN a2enmod headers


# LINK apache config to docker logs.
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/1 /var/log/apache2/error.log

EXPOSE 80

WORKDIR /var/www/apache-flask

CMD  /usr/sbin/apache2ctl -D FOREGROUND
