#! /bin/bash

# Start the Postgres database.
service postgresql start
counter=0
until pg_isready -q
do
    sleep 1
    ((counter += 1))
done
echo Postgres took approximately $counter seconds to fully start ...

# Set up iRODS.
python3 /var/lib/irods/scripts/setup_irods.py < /irods_provider.input
service irods start

su irods -c '/demosetup.sh'
echo Completed Setup

# Keep container running if the test fails.
tail -f /dev/null
# Is this better? sleep 2147483647d

© 2020 GitHub, Inc.

