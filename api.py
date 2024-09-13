from flask import Blueprint, request, jsonify
from bson import json_util, ObjectId
import json

def register_routes(app):
    api_blueprint = Blueprint('api', __name__)

    # Helper function to convert BSON to JSON
    def bson_to_json(data):
        return json.loads(json_util.dumps(data))

    # 1. GET - Retrieve all documents
    @api_blueprint.route('/documents', methods=['GET'])
    def get_documents():
        results = app.config['collection'].find()
        documents = bson_to_json(results)
        response = {
            "status": 200,
            "data": documents
        }
        return jsonify(response)

    # 2. GET - Retrieve a specific document by ID
    @api_blueprint.route('/documents/<id>', methods=['GET'])
    def get_document_by_id(id):
        document = app.config['collection'].find_one({"_id": ObjectId(id)})
        if document:
            response = {
                "status": 200,
                "data": bson_to_json(document)
            }
        else:
            response = {
                "status": 404,
                "message": "Document not found"
            }
        return jsonify(response)

    # 3. POST - Create a new document
    @api_blueprint.route('/documents', methods=['POST'])
    def create_document():
        data = request.json
        result = app.config['collection'].insert_one(data)
        new_document = app.config['collection'].find_one({"_id": result.inserted_id})
        response = {
            "status": 201,
            "data": bson_to_json(new_document)
        }
        return jsonify(response), 201

    # 4. PUT - Update an existing document by ID
    @api_blueprint.route('/documents/<id>', methods=['PUT'])
    def update_document(id):
        data = request.json
        result = app.config['collection'].update_one({"_id": ObjectId(id)}, {"$set": data})
        
        if result.matched_count:
            updated_document = app.config['collection'].find_one({"_id": ObjectId(id)})
            response = {
                "status": 200,
                "data": bson_to_json(updated_document)
            }
        else:
            response = {
                "status": 404,
                "message": "Document not found"
            }
        return jsonify(response)

    # 5. DELETE - Delete a document by ID
    @api_blueprint.route('/documents/<id>', methods=['DELETE'])
    def delete_document(id):
        result = app.config['collection'].delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count:
            response = {
                "status": 200,
                "message": "Document deleted successfully"
            }
        else:
            response = {
                "status": 404,
                "message": "Document not found"
            }
        return jsonify(response)

    app.register_blueprint(api_blueprint)
