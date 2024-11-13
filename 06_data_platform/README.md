# iRODS/Metalnx Docker

A persistent data, disposable docker container approach to iRods with a Metalnx Web GUI

## Build

The iRods Server config can be set in the [config.sh](./iRods/config.sh) environment file. 
Afterwards setup inputs for the provider and consumer can be created by running [geninput.sh](./iRods/geninput.sh).
Currently [metalnx.properties](./Metalnx/conf/metalnx.properties) has to be manually changed (WIP: also use the config.sh environment file to generate this).

iRods and Metalnx are in two different docker compose files. To build either change into the repsective directory and execute:
```bash
$ docker compose build
```

## Startup

First startup the iRods containers:
```bash
$ cd ./iRods
$ docker compose up
```
Wait for iRods to setup. When both `irods-catalog-provider` and `irods-catalog-consumer-resource1` echo "Completed Setup" in the terminal, Metalnx is safe to start via:
```bash
$ cd ../Metalnx
$ docker compose up
```
Afterwards open http://localhost/metalnx/ on the machine (WIP: will be put behind a reverse proxy)


## Container Overview

- `irodsnet`: a network over which containers can communicate on the host machine run in bridge mode
- `irods-catalog-provider`: the iRODS 4.3.0 provider server, also running the (persistent) PostgreSQL iCAT database, with a persistent storage resource mounted to [Vault](./Vault)
- `irods-catalog-consumer-resource1`: an iRODS 4.3.0 resource server, only reachable via the irods-catalog-provider
- `metalnx-database`: a (persistent) PostgreSQL database for metalnx
- `metalnx`: Metalnx docker container configured via the files in the [conf](./Metalnx/conf) directory

## Demo info

### File sharing

Permission Inheritence always defaults to the *strictest* rule: e.g. if user A shares a file in their home directory with user B, user B will see the file under "Shared Links", but will get a permissions error, when clicking on it. Therefore, to share the file user A needs to create a directory *without* inhertience (disabled by default, but can be activated by the user via a tick in the "Add Collection" dialogue) and share it with user B. This will NOT share files in the directory (just grant access to the general file path; accessing another file in the directory e.g. via a direkt link will yield a "Access Denied" message). Therfore files still have to be shared individually (or via ticking "Apply to subcollections and files" in the permissions dialogues). 