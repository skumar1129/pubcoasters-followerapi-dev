from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_sslify import SSLify
import os
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{Config.credentials['username']}:{Config.credentials['password']}@/{Config.credentials['schema']}?unix_socket=/cloudsql/{Config.credentials['connectionname']}"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sahil23!@localhost/app_localdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors = CORS(app)
migrate = Migrate(app, db)
sslify = SSLify(app)

from service.follower_service import FollowerService as follower_service

@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    return jsonify({'message': 'test works'})


@app.route('/follower', methods=['POST', 'DELETE'])
@cross_origin()
def follower():
    if request.method == 'POST':
        return follower_service().createFollowing(body=request.json)
    elif request.method == 'DELETE':
        return follower_service().deleteFollowing(body=request.json)
    
@app.route('/allfollowers', methods=['GET'])
@cross_origin()
def allfollower():
    user = request.headers.get('user')
    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)
    return follower_service().getAllFollowers(user=user, page=page)

@app.route('/allfollowing', methods=['GET'])
@cross_origin()
def allfollowing():
    user = request.headers.get('user')
    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)
    return follower_service().getAllFollowing(user, page)

@app.route('/userfollowers/<string:user>', methods=['GET'])
@cross_origin()
def userfollowers(user):
    my_user = request.headers.get('user')
    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)
    return follower_service().getAllUserFollowers(user=user, my_user=my_user, page=page)

@app.route('/userfollowing/<string:user>', methods=['GET'])
@cross_origin()
def userfollowing(user):
    my_user = request.headers.get('user')
    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)
    return follower_service().getAllUserFollowing(user=user, my_user=my_user, page=page)

@app.route('/followingposts', methods=['GET'])
@cross_origin()
def followingposts():
    user = request.headers.get('user')
    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)
    return follower_service().getFollowingPosts(user=user, page=page)