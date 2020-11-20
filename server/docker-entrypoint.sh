#!/bin/bash

set -eu

variables='${SERVER_PORT}
          ${API_DOMAIN}
          ${API_HOSTNAME}
          ${API_PORT}
          ${CLUSTER_HOSTNAME}
          ${CLUSTER_MANAGER_PORT}
          ${CLUSTER_NODE_PORT}
          ${CLUSTER_NETWORK_PORT}
          ${REGISTRY_DOMAIN}
          ${REGISTRY_HOSTNAME}
          ${REGISTRY_PORT}
          ${STORAGE_DOMAIN}
          ${STORAGE_HOSTNAME}
          ${STORAGE_PORT}
          ${TASK_QUEUE_HOSTNAME}
          ${TASK_QUEUE_PORT}'

envsubst "$variables" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec "$@"
