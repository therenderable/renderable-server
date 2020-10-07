#!/bin/bash

set -eu

variables='${SERVER_PORT}
          ${API_DOMAIN}
          ${API_HOSTNAME}
          ${API_PORT}
          ${CLUSTER_DOMAIN}
          ${CLUSTER_HOSTNAME}
          ${CLUSTER_MASTER_PORT}
          ${CLUSTER_NODE_PORT}
          ${CLUSTER_NETWORK_PORT}
          ${STORAGE_DOMAIN}
          ${STORAGE_HOSTNAME}
          ${STORAGE_PORT}
          ${QUEUE_HOSTNAME}
          ${QUEUE_PORT}'

envsubst "$variables" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec "$@"
