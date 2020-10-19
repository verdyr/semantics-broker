#!/bin/bash

HOST_NAME=$1

HOST_PORT=$2

FILE_OR_DIR=$3

NSS_PROPERTIES=$4

LOAD_PROP_FILE=/tmp/$$.properties

[ -z "${NSS_PROPERTIES}" ] && export NSS_PROPERTIES=$(pwd)/RWStore.properties

cat <<EOT >> $LOAD_PROP_FILE
quiet=false
verbose=0
closure=false
durableQueues=true
#Needed for quads
#defaultGraph=
com.bigdata.rdf.store.DataLoader.flush=false
com.bigdata.rdf.store.DataLoader.bufferCapacity=100000
com.bigdata.rdf.store.DataLoader.queueCapacity=10
#Namespace to load
namespace=kb
#Files to load
fileOrDirs=$1
#Property file (if creating a new namespace)
propertyFile=$NSS_PROPERTIES
EOT

echo "Loading with properties..."

cat $LOAD_PROP_FILE

curl -X POST --data-binary @${LOAD_PROP_FILE} --header 'Content-Type:text/plain' http://$HOST_NAME:$HOST_PORT/blazegraph/dataloader

#Let the output go to STDOUT/ERR to allow script redirection

rm -f $LOAD_PROP_FILE
