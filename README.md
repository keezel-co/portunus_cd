# portunus_cd
This tool requires Portunus API - https://github.com/keezel-co/portunus_api

# Portunus Config Deliverer - Wireguard provisioning tool
Portunus is a set of tools that make it easy to deploy and manage Wireguard servers and clients at scale.
This `portunus_cd` repository contains the `Config Deliverer` for `portunus_api`. This is a stripped down
version of `portunus_api` that only allows calls to `GET` a config for a server (if the correct server token is presented)
and to register your server with the API (for automatic creation and deletion of clients through SSH)

# Quick installation
If you want to go the full provisioning route, you're probably best off running the `portunus_docker` container which will
install `portunus_api` and `portunus_cd` on the same machine with TLS, shared database, etc. Go check it out here: https://github.com/keezel-co/portunus_docker/

# Installation
Make sure you have `Docker` and `docker-composer` installed on your system. Make sure you configure the database you want to 
connect to in `config.py`. 

1. `git clone https://github.com/keezel-co/portunus_cd`
2. `cd portunus_cd && docker-compose up --build`
