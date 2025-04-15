# Use official Perl image as base
FROM perl:5.34

# Install Apache and necessary Perl modules
RUN apt-get update && \
    apt-get install -y apache2 libapache2-mod-perl2 libdbi-perl libdbd-mysql-perl && \
    a2enmod cgi

# Set working directory
WORKDIR /var/www/html

# Copy your Perl CGI scripts into the web root
COPY ./src /var/www/html

# Ensure scripts are executable
RUN chown -R www-data:www-data /var/www/html && \
    chmod +x /var/www/html/*.cgi

# Expose port 80
EXPOSE 80

# Run Apache in the foreground
CMD ["apachectl", "-D", "FOREGROUND"]
