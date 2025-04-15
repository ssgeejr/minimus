# Use official Perl image with Debian base
FROM perl:5.34

# Install Apache, CGI support, and Perl modules
RUN apt-get update && \
    apt-get install -y apache2 libapache2-mod-perl2 libdbi-perl libdbd-mysql-perl && \
    a2enmod cgi && \
    cpan install CGI

# Set the working directory to the web root
WORKDIR /var/www/html

# Copy your CGI scripts into the web root
COPY ./src /var/www/html

# Copy custom Apache config to enable CGI
COPY apache2/apache-cgi.conf /etc/apache2/sites-available/000-default.conf

# Ensure scripts are executable and readable
RUN chmod -R 755 /var/www/html && \
    chown -R www-data:www-data /var/www/html

# Silence Apache warning about ServerName
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Expose HTTP port
EXPOSE 80

# Start Apache in the foreground
CMD ["apachectl", "-D", "FOREGROUND"]
