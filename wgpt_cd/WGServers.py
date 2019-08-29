import ipaddress, subprocess
import socket
from flask import request, Response, abort
from flask_restful import Resource
from marshmallow import ValidationError
from wgpt_cd.models import db, Client, Server, ClientSchema, ServerSchema, Cluster, ClusterSchema

client_schema = ClientSchema(many=True)
server_schema = ServerSchema()
servers_schema = ServerSchema(many=True)


class GetServerConfig(Resource):
    def post(self, server_id):

        json_data = request.get_json(force=True)
        if not json_data:
            return {'status':'failure', 'message':'No input data provided'}, 400

        if not json_data['token']:
            return {'status':'failure', 'message':'No input data provided'}, 400

        server = Server.query.filter_by(server_token=json_data['token']).first()
        if not server:
            return {'status':'failure', 'message':'No valid token provided'}, 400

        if server.cluster_id:
            return {'status':'failure', 'message':'this server is part a cluster, use /api/clusters/get/config/<int:cluster_id> instead'}

        print(server)

        clients = Client.query.filter_by(server_id=server_id).all()
        config=''
        config += '[Interface]\n'
        if server.server_networkv4 and server.server_networkv6:
            config += 'Address = ' + server.server_networkv4 + ', ' + server.server_networkv6 +'\n'
        if server.server_networkv4 and not server.server_networkv6:
            config += 'Address = ' + server.server_networkv4 +'\n'
        if server.server_networkv6 and not server.server_networkv4:
            config += 'Address = ' + server.server_networkv6 +'\n'
        config += 'PrivateKey = ' + server.server_privkey +'\n'
        config += 'ListenPort = ' + str(server.server_port) +'\n'
        if server.server_postup:
            config += 'PostUp = ' + str(server.server_postup) +'\n'
        if server.server_postdown:
            config += 'PostDown = ' + str(server.server_postdown) +'\n'
        config += '\n'

        for client in clients:
            config += '[Peer]\n'
            config += 'PublicKey = ' + client.client_pubkey + '\n'
            if client.client_ipv4 and client.client_ipv6:
                config += 'AllowedIPs = ' + client.client_ipv4 + ',' + client.client_ipv6 + '\n'
            if client.client_ipv4 and not client.client_ipv6:
                config += 'AllowedIPs = ' + client.client_ipv4 + '\n'
            if not client.client_ipv4 and client.client_ipv6:
                config += 'AllowedIPs = ' + client.client_ipv6 + '\n'
            config += '\n'

        return Response(config, mimetype='text')