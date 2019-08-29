import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'wgpt.db')
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_RECYCLE = 280
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wgpt:yoursecretpassword@127.0.0.1/wgpt'
    CERT_SSL_CA = os.path.join(basedir, os.environ.get('CERT_SSL_CA') or 'certs/ca-cert.pem')
    CERT_SSL_CA_KEY = os.path.join(basedir, os.environ.get('CERT_SSL_CA_KEY') or 'certs/ca-key.pem')
