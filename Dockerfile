# Use official Perl image with Debian base
FROM perl:5.34

# Install Apache, CGI support, and all required Perl modules via apt
RUN apt-get update && \
    apt-get install -y \
        apache2 \
        libapache2-mod-perl2 \
        libdbi-perl \
        libdbd-mysql-perl \
        libcgi-pm-perl && \
    a2enmod cgi

# Set working directory
WORKDIR /var/www/html

# Copy CGI scripts to the web root
COPY ./src /var/www/html

# Copy Apache config to enable CGI
COPY apache2/apache-cgi.conf /etc/apache2/sites-available/000-default.conf

# Ensure scripts are executable and owned properly
RUN chmod -R 755 /var/www/html && \
    chown -R www-data:www-data /var/www/html

# Suppress Apache FQDN warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Expose HTTP port
EXPOSE 80

# Run Apache in foreground
CMD ["apachectl", "-D", "FOREGROUND"]
