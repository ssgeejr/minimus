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

# Copy your CGI scripts into the web root
COPY ./src /var/www/html
RUN mkdir /var/www/html/adobe
COPY ./adobe /var/www/html/adobe/

# Copy Apache config to enable CGI
COPY apache2/apache-cgi.conf /etc/apache2/sites-available/000-default.conf

# Copy CSS (if not already done by previous COPY)
#COPY ./src/style.css /var/www/html/style.css

# Ensure scripts are executable and readable
RUN find /var/www/html -name "*.cgi" -exec chmod 755 {} \; && \
    chown -R www-data:www-data /var/www/html

RUN chmod -R g+w /var/www/html/index.cgi
RUN chown www-data:www-data /var/www/html/*

# Suppress Apache FQDN warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Expose HTTP port
EXPOSE 80

# Run Apache in the foreground
CMD ["apachectl", "-D", "FOREGROUND"]
