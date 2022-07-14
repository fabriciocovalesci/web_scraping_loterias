#!/bin/bash

# build image
docker build -t loteria_bot . 

# change tag recent
docker tag loteria_bot:latest fabriciocov/loteria_bot:latest

# Push to repository - docker hub
docker push fabriciocov/loteria_bot:latest