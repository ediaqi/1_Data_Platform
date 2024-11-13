#!/bin/bash

DB_INIT="db.init"                                             # SQL Commands to init ICAT DB
PROVIDER_INPUT="irods_provider.input"                         # Provider Setup Input File
CONSUMER_INPUT="irods_consumer.input"                         # Consumer Setup Input File
IRODS_SERVICE_USER="irods"                                    # Service Account User ID
IRODS_SERVICE_GROUP="irods"                                   # Service Account Group ID     
IRODS_ICAT_DBSERVER="localhost"                               # ICAT DB Server hostname or IP address
IRODS_ICAT_DBPORT="5432"                                      # ICAT DB Server Port
IRODS_ICAT_DBNAME="ICAT"                                      # ICAT DB Name
IRODS_ICAT_DBUSER="admin"                                     # ICAT DB User ID
IRODS_ICAT_DBPASS="ppp"                              # ICAT DB Password
IRODS_ICAT_RESOURCE="demoResc"                                # ICAT Default Resource
IRODS_ICAT_RESOURCE1="demoResc1"                              # Resource Server Default Resource
IRODS_ICAT_VAULT="/var/lib/irods/Vault"                       # ICAT Default Vault
IRODS_ZONE_NAME="ediaqi"                                      # Zone Name
IRODS_ICAT_HOST="icat.know-center.at"                         # ICAT Provider Server hostname or IP address
IRODS_ZONE_PORT="1247"                                        # Zone Port
IRODS_DATA_PORT_RANGE_BEG="20000"                             # Transport Starting Port
IRODS_DATA_PORT_RANGE_END="20199"                             # Transport Ending Port
IRODS_CONTROLPLANE_PORT="1248"                                # Control Plane Port
SCHEMA_URI="file:///var/lib/irods/configuration_schemas"      # Schema Validation URI
IRODS_ADMIN_USER="admin"                                       # Admin Account Name
IRODS_ZONE_KEY="TEMPORARY_ZONE_KEY"                           # Zone Key
IRODS_NEGOTIATION_KEY="32_byte_server_negotiation_key__"      # Negotiation Key
IRODS_CONTROLPLANE_KEY="32_byte_server_control_plane_key"     # Control Plane Key
IRODS_ADMIN_PASS=""                                       # Admin Account Password
