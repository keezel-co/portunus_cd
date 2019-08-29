from flask import Blueprint, send_from_directory
from flask_restful import Api
from wgpt_cd import app, db, api

from wgpt_cd.WGServers import *
from wgpt_cd.WGClusters import *
from wgpt_cd.WGRegister import * 

# Register
api.add_resource(Register, '/api/register')

# Servers
api.add_resource(GetServerConfig, '/api/servers/get/config/<int:server_id>')

# Clusters
api.add_resource(GetClusterConfig, '/api/clusters/get/config/<int:cluster_id>')

api.init_app(app)