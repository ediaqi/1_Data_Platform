#!/bin/sh
iadmin mkresc test1-resc unixfilesystem $HOSTNAME:/var/lib/irods/iRODS/Vault1

iadmin mkresc test1-resc2 unixfilesystem $HOSTNAME:/var/lib/irods/iRODS/Vault2

iadmin mkresc test1-resc3 unixfilesystem $HOSTNAME:/var/lib/irods/iRODS/Vault3

iadmin atg public anonymous

iadmin mkgroup jargonTestUg

iadmin atg jargonTestUg test1

iadmin atg jargonTestUg test3

