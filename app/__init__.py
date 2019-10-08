from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request , jsonify, abort


#local import 
from instance.config import app_config

# initilize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import Bucketlist

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)



    @app.route('/bucketlists/', methods=['GET'])
    def get_bucketlists():
        bucketlists = Bucketlist.get_all()
        results = []
        for bucketlist in bucketlists:
            obj = {
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response


    @app.route('/bucketlists/', methods=['POST'])
    def bucketlists():
        name = str(request.data.get('name', ''))
        if name:
            bucketlist = Bucketlist(name=name)
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified 
            })
            response.status_code = 201
            return response
    
    @app.route('/bucketlists/<int:id>', methods=['GET'])
    def get_single_bucketlist(id, **kwargs):
        # Retrieve a bucketlist using its ID
        print(id)
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)
        response = jsonify({
            'id': bucketlist.id,
            'name': bucketlist.name,
            'date_created': bucketlist.date_created,
            'date_modified': bucketlist.date_modified
        })
        response.status_code = 200
        return response

    @app.route('/bucketlists/<int:id>', methods=['PUT'])
    def update_a_given_bucketlist(id):
        # Update a given bucketlist
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)
        name = str(request.data.get('name', ''))
        bucketlist.name = name
        bucketlist.save()
        response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
        response.status_code = 200
        return response

    @app.route('/bucketlists/<int:id>', methods=['DELETE'])
    def delete_a_given_bucketlist(id):
        # Delete a given bucketlist
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)
        bucketlist.delete()
        response = jsonify({
           "message": "bucketlist {} deleted successfully".format(bucketlist.id)      
        })
        response.status_code = 200
        return response

    

               
    return app