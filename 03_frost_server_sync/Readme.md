# FROST-Server, Software Sync tools

## Deployment FROST-Server with Projects plugin
kdpplugin is configured for the ediaqi VM server. Make sure that keycloak is already up and running.

The plugin can be installed with following steps:

1. Start in the docker compose with `auth_provider=de.fraunhofer.iosb.ilt.frostserver.auth.basic.BasicAuthProvider`
2. go into `docker exec -it <postgres_container_id> psql -U <username>`
3. paste in psql: `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`
4. Hit in Frost-Server web home, Database Status, the Update button
5. paste in psql: `ALTER TABLE "USERS" ALTER COLUMN "USER_NAME" TYPE VARCHAR(64) USING "USER_NAME";`
6. Change in docker compose to `auth_provider=de.fraunhofer.iosb.ilt.frostserver.auth.keycloak.KeycloakAuthProvider`
7. Accounts can be created over keycloak

## Demo data for Data Ingestion
Example data for each entity is provided in the `demo_simple_entities` folder.

## Sync multiple FROST-Servers
Collection of diverse python scripts that synchronize the contents between them. They utilize MQTT or HTTP requests. Just provide authentification and modify URLs in these scripts to query a target FROST-Server and transfer the batches of data to the destination FROST-Server.