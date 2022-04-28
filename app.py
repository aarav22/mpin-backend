from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import os

# Charm
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.schemes.ibenc.ibenc_bf01 import IBE_BonehFranklin
from charm.toolbox.IBEnc import IBEnc
from charm.toolbox.hash_module import Hash,int2Bytes,integer
import json

verify = [51, 58, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 69, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65]

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
group = PairingGroup('BN254')

def to_json(python_object):                           
        return {'__class__': 'bytes',
                '__value__': list(python_object)}   
class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), unique=True, nullable=False)
  content = db.Column(db.String(120), unique=True, nullable=False)

  def __init__(self, title, content):
    self.title = title
    self.content = content

# class for holding secrets: TA and Server
class Secrets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.ARRAY(db.Integer), unique=True, nullable=False)
    key = db.Column(db.ARRAY(db.Integer), unique=True, nullable=True)
    def __init__(self, name, secret, key):
        self.name = name
        self.secret = secret
        self.key = key


class Authentication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    U = db.Column(db.ARRAY(db.Integer), nullable=False)
    y = db.Column(db.ARRAY(db.Integer), nullable=False)
    def __init__(self, user_id, U, y):
        self.user_id = user_id
        self.U = U
        self.y = y

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    def __init__(self, user_id):
        self.user_id = user_id

db.create_all()

''' TA '''

''' Store
 * Master Secret
'''

''' Routes
 * Get client secret
 * Get server secret
'''


# to store master secret in db
@app.route('/init-ta', methods=['GET'])
def create_TA():
    name = "Master"
    master_secret = group.random(ZR)
    master_secret_ser = group.serialize(master_secret)
    secret = list(master_secret_ser)
    try:
        db.session.query(Secret).filter_by(name="Master").delete()
        db.session.commit()
    except:
        db.session.rollback()

    db.session.add(Secrets(name, secret, None))
    db.session.commit()
    return "TA created"

# to store server secret  and server pkey in db
# TODO: Also store the server key
@app.route('/init-server', methods=['GET'])
def create_server():
    name = "Server"
    server_key = group.random(G2)

    master_secret_ser = db.session.query(Secrets).filter_by(name="Master")
    master_secret = group.deserialize(bytes(master_secret_ser[0].secret))
    
    server_key_ser = group.serialize(server_key)
    server_key_ser_list = list(server_key_ser)

    server_secret = server_key * master_secret
    server_secret_ser = group.serialize(server_secret)
    secret = list(server_secret_ser)

    try:
        db.session.query(Secret).filter_by(name="Server").delete()
        db.session.commit()
    except:
        db.session.rollback()

    db.session.add(Secrets(name, secret, server_key_ser_list))
    db.session.commit()
    return "Server created"
    

# TODO: Verify the email using OTP
@app.route('/client-secret', methods=['POST'])
def get_client_secret():
    body = request.get_json()
    master_secret_ser = db.session.query(Secrets).filter_by(name="Master")
    master_secret = group.deserialize(bytes(master_secret_ser[0].secret))
    A = group.deserialize(bytes(body['A_ser']['__value__']))
    id = body['id']

    # save client id in db if not already present:
    try:
        db.session.query(Clients).filter_by(user_id=id).one()
    except:
        db.session.add(Clients(id))
        db.session.commit()

    client_secret = master_secret * A
    cs_ser = group.serialize(client_secret)
    res = json.dumps(cs_ser, default=to_json) 
    return res

# TODO: Implement this
# @app.route('/server-secret', methods=['POST'])
# def get_server_secret():
#     body = request.get_json()
#     master_secret = db.session.query(Secrets).filter_by(name="Master")
#     Q = group.deserialize(bytes(body['Q_ser']['__value__']))
#     server_secret = master_secret * Q
#     ss_ser = group.serialize(server_secret)
#     res = json.dumps(ss_ser, default=to_json) 
#     return res

''' End of TA Routes '''

''' Server '''

''' Store
 * Server Secret
 * Client Identity
 * For each client authentication:
  *   U
''' 

''' Routes
 * Send 'y' to client after receiving id and U
 * Authenticate client given id, U and V.
 * Get server secret
'''

''' Server Routes '''
# route to store server secret in db
# @app.route('/server-secret', methods=['GET'])
# def store_server_secret():
#     res = get_server_secret()
#     server_secret = group.deserialize(bytes(res))
#     print(server_secret)
#     return "Server Secret stored"

# route to get random number 'y':
@app.route('/get-y', methods=['POST'])
def get_y():
    body = request.get_json()

    # extract id and U from body
    id = body['id']
    U_ser_list = body['U_ser']['__value__']
    y = group.random(ZR)
    y_ser = group.serialize(y)
    y_ser_list = list(y_ser)

    # check if id exists in Authentication table
    try:
        db.session.query(Authentication).filter_by(user_id=id).one()
    except:
        db.session.add(Authentication(id, U_ser_list, y_ser_list))
        db.session.commit()


    res = json.dumps(y_ser, default=to_json) 
    return res

# to authenticate client:
@app.route('/authenticate', methods=['POST'])
def authenticate():
    body = request.get_json()
    V_ser_list = body['V_ser']['__value__']
    id = body['id']
    A = group.hash(id, G1)


    # get U, server_key, server_secret and y from db
    U_ser_list = db.session.query(Authentication).filter_by(user_id=id)
    U = group.deserialize(bytes(U_ser_list[0].U))
    V = group.deserialize(bytes(V_ser_list))
    y_ser_list = db.session.query(Authentication).filter_by(user_id=id)
    y = group.deserialize(bytes(y_ser_list[0].y))
    server_res = db.session.query(Secrets).filter_by(name="Server")
    server_secret = group.deserialize(bytes(server_res[0].secret))
    server_key = group.deserialize(bytes(server_res[0].key))

    # compute g:
    g=pair(V, server_key) * pair(U + y*A, server_secret)
    return list(group.serialize(g)) == verify
