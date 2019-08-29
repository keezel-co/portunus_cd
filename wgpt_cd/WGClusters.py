import ipaddress, subprocess
from flask import request, Response, abort
from flask_restful import Resource
from marshmallow import Schema, fields, pre_load, validate, ValidationError
from wgpt_cd.models import db, Client, Server, Cluster, ClientSchema, ServerSchema, ClusterSchema

client_schema = ClientSchema()
server_schema = ServerSchema()
cluster_schema = ClusterSchema()
clusters_schema = ClusterSchema(many=True)


class GetClusterConfig(Resource):
    def post(self, cluster_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status':'failure', 'message':'No input data provided'}, 400

        if not json_data['token']:
            return {'status':'failure', 'message':'No input data provided'}, 400

        server = Server.query.filter_by(server_token=json_data['token']).first()
        if not server:
            return {'status':'failure', 'message':'No valid token provided'}, 400

        cluster = Cluster.query.filter_by(id=cluster_id).first()
        if not cluster:
            return {'status':'failure', 'message':'no cluster by that id'}

        clients = cluster.clients
        config=''
        config += '[Interface]\n'
        if cluster.cluster_networkv4 and cluster.cluster_networkv6:
            config += 'Address = ' + cluster.cluster_networkv4 + ', ' + cluster.cluster_networkv6 + '\n'
        if cluster.cluster_networkv4 and not cluster.cluster_networkv6:
            config += 'Address = ' + cluster.cluster_networkv4 + '\n'
        if cluster.cluster_networkv6 and not cluster.cluster_networkv4:
            config += 'Address = ' + cluster.cluster_networkv6 + '\n'
        config += 'PrivateKey = ' + cluster.cluster_privkey +'\n'
        config += 'ListenPort = ' + str(cluster.cluster_port) +'\n'
        config += '\n'

        for client in clients:
            config += '[Peer]\n'
            config += 'PublicKey = ' + client.client_pubkey + '\n'
            if client.client_ipv4 and client.client_ipv6:
                config += 'AllowedIPs = ' + client.client_ipv4 + ',' + client.client_ipv6 + '\n'
            if client.client_ipv4 and not client.client_ipv6:
                config += 'AllowedIPs = ' + client.client_ipv4 + '\n'
            if client.client_ipv6 and not client.client_ipv4:
                config += 'AllowedIPs = ' + client.client_ipv6 + '\n'
            config += '\n'
        print(config)
        return Response(config, mimetype='text')
