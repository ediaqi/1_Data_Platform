#!/bin/bash

source config.sh

### ICAT Database Init commands ###################################################################
echo "CREATE DATABASE \"$IRODS_ICAT_DBNAME\";" > $DB_INIT
echo "CREATE USER $IRODS_ICAT_DBUSER WITH PASSWORD '$IRODS_ICAT_DBPASS';" >> $DB_INIT
echo "GRANT ALL PRIVILEGES ON DATABASE \"$IRODS_ICAT_DBNAME\" to $IRODS_ICAT_DBUSER;" >> $DB_INIT
echo "\q" >> $DB_INIT
echo "" >> $DB_INIT
### ICAT Database Init commands ###################################################################


### Provider ######################################################################################
# Service Account
echo $IRODS_SERVICE_USER > $PROVIDER_INPUT              # user ID
echo $IRODS_SERVICE_GROUP >> $PROVIDER_INPUT            # group ID
echo "1" >> $PROVIDER_INPUT                             # service role (provider)

# Database Connection
echo "1" >> $PROVIDER_INPUT                             # driver (PostgreSQL ANSI)
echo $IRODS_ICAT_DBSERVER >> $PROVIDER_INPUT            # host
echo $IRODS_ICAT_DBPORT >> $PROVIDER_INPUT              # port
echo $IRODS_ICAT_DBNAME >> $PROVIDER_INPUT              # name
echo $IRODS_ICAT_DBUSER >> $PROVIDER_INPUT              # user
echo "y" >> $PROVIDER_INPUT                             # confirm
echo $IRODS_ICAT_DBPASS >> $PROVIDER_INPUT              # password
echo "DCCN" >> $PROVIDER_INPUT                          # password salt

# Local Storage
echo "y" >> $PROVIDER_INPUT                             # enable
echo $IRODS_ICAT_RESOURCE >> $PROVIDER_INPUT            # default resource
echo $IRODS_ICAT_VAULT >> $PROVIDER_INPUT               # defautl vault path

# iRODS Server Options
echo $IRODS_ZONE_NAME >> $PROVIDER_INPUT                # zone name
echo $IRODS_ZONE_PORT >> $PROVIDER_INPUT                # zone port 
echo $IRODS_DATA_PORT_RANGE_BEG >> $PROVIDER_INPUT      # transport starting port #
echo $IRODS_DATA_PORT_RANGE_END >> $PROVIDER_INPUT      # transport ending port #
echo $IRODS_CONTROLPLANE_PORT >> $PROVIDER_INPUT        # control plane port
echo $SCHEMA_URI >> $PROVIDER_INPUT                     # schema validation URI
echo $IRODS_ADMIN_USER >> $PROVIDER_INPUT               # iRODS admin account name
echo "y" >> $PROVIDER_INPUT                             # confirm

# Keys and Passwords
echo $IRODS_ZONE_KEY >> $PROVIDER_INPUT                 # zone key
echo $IRODS_NEGOTIATION_KEY >> $PROVIDER_INPUT          # negotiation key
echo $IRODS_CONTROLPLANE_KEY >> $PROVIDER_INPUT         # control plane key
echo $IRODS_ADMIN_PASS >> $PROVIDER_INPUT               # iRODS admin account password
### Provider ######################################################################################


### Consumer ######################################################################################
# Service Account
echo "irods" > $CONSUMER_INPUT                          # user ID
echo "irods" >> $CONSUMER_INPUT                         # group ID
echo "2"     >> $CONSUMER_INPUT                         # service role (consumer)

# Local Storage
echo "y" >> $CONSUMER_INPUT                             # enable
echo $IRODS_ICAT_RESOURCE1 >> $CONSUMER_INPUT           # default resource
echo $IRODS_ICAT_VAULT >> $CONSUMER_INPUT               # defautl vault path

# iRODS Server Options
echo $IRODS_ZONE_NAME >> $CONSUMER_INPUT                # zone name
echo $IRODS_ICAT_HOST >> $CONSUMER_INPUT                # iCAT server
echo $IRODS_ZONE_PORT >> $CONSUMER_INPUT                # zone port 
echo $IRODS_DATA_PORT_RANGE_BEG >> $CONSUMER_INPUT      # transport starting port #
echo $IRODS_DATA_PORT_RANGE_END >> $CONSUMER_INPUT      # transport ending port #
echo $IRODS_CONTROLPLANE_PORT >> $CONSUMER_INPUT        # control plane port
echo $SCHEMA_URI >> $CONSUMER_INPUT                     # schema validation URI
echo $IRODS_ADMIN_USER >> $CONSUMER_INPUT               # iRODS admin account name
echo "y" >> $CONSUMER_INPUT                             # confirm

# Keys and Passwords
echo $IRODS_ZONE_KEY >> $CONSUMER_INPUT                 # zone key
echo $IRODS_NEGOTIATION_KEY >> $CONSUMER_INPUT          # negotiation key
echo $IRODS_CONTROLPLANE_KEY >> $CONSUMER_INPUT         # control plane key
echo $IRODS_ADMIN_PASS >> $CONSUMER_INPUT               # iRODS admin account password
### Consumer ######################################################################################