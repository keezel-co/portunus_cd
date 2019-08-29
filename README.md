# cableguard_cd
This tool requires Cableguard API - https://github.com/keezel-co/cableguard_api

#Cableguard Config Deliverer - Wireguard provisioning tool
Cableguard is a set of tools that make it easy to deploy and manage Wireguard servers and clients at scale.
This `cableguard_cd` repository contains the `Config Deliverer` for `cableguard_api`. This is a stripped down
version of `cableguard_api` that only allows calls to `GET` a config for a server (if the correct server token is presented)
and to register your server with the API (for automatic creation and deletion of clients through SSH)

# Quick installation
If you want to go the full provisioning route, you're probably best off running the `cableguard_docker` container which will
install `cableguard_api` and `cableguard_cd` on the same machine with TLS, shared database, etc. Go check it out here: https://github.com/keezel-co/cableguard_docker/

# Installation
Make sure you have `Docker` and `docker-composer` installed on your system. Make sure you configure the database you want to 
connect to in `config.py`. 

1. `git clone https://github.com/keezel-co/cableguard_cd`
2. `cd cableguard_cd && docker-compose up --build`
