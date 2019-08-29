import base64

from flask import request, Response, abort
from flask_restful import Resource
from wgpt_cd.models import db, Server, ConfigOptions
from wgpt_cd import WGGencert
from wgpt_cd import app

class Register(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status':'failure', 'message':'No input data provided'}, 400

        server_token = json_data['server_token']
        server_ssh_key = json_data['server_ssh_key']
        
        server = Server.query.filter_by(server_token=server_token).first()
        if not server:
            abort(404)

        # insert the ssh key
        server.server_ssh_key = server_ssh_key
        db.session.commit()

        # Fetch the ssh key
        co = ConfigOptions.query.first()

        # Generate the certs
        certs = WGGencert.generate_cert_signed_with_ca(server.server_description, app.config['CERT_SSL_CA'], app.config['CERT_SSL_CA_KEY'])
        if not certs:
            return {'status': 'failure', 'message': 'cannot generate certificates'}

        return {'status': 'success',
                'cert': base64.b64encode(certs[0]).decode('ascii'),
                'key': base64.b64encode(certs[1]).decode('ascii'),
                'ca': base64.b64encode(certs[2]).decode('ascii'),
                'ssh': co.ssh_pubkey,
                'server': server.id}

