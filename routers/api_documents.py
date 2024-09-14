import os
from flask import Blueprint, request
from pymongo import MongoClient
from bson import json_util, ObjectId
from common.utils import create_response, bson_to_json
from middlewares.auth_middleware import token_required

# Create a Blueprint for document-related routes
api_documents = Blueprint('api_documents', __name__)

# Get the MongoDB URI from environment variables
connection_string = os.getenv('AZURE_CONNECTION_URI')
db_name = os.getenv('DB_NAME')
collection_id = os.getenv('COLLECTION_ID')

# Check if environment variables are set
if not connection_string or not db_name or not collection_id:
    raise ValueError("Missing environment variables for MongoDB configuration.")

# MongoDB setup
try:
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_id]
except Exception as e:
    raise RuntimeError(f"Failed to connect to MongoDB: {e}")

# GET route to retrieve all documents
@api_documents.route('/documents', methods=['GET'])
@token_required
def get_documents():
    results = collection.find()
    documents = bson_to_json(results)
    return create_response(200, data=documents)

# GET route to retrieve a document by its ID
@api_documents.route('/documents/<id>', methods=['GET'])
@token_required
def get_document_by_id(id):
    document = collection.find_one({"_id": ObjectId(id)})
    if document:
        return create_response(200, data=bson_to_json(document))
    return create_response(404, message="Document not found")

# POST route to create a new document
@api_documents.route('/documents', methods=['POST'])
@token_required
def create_document():
    data = request.json
    result = collection.insert_one(data)
    new_document = collection.find_one({"_id": result.inserted_id})
    return create_response(201, data=bson_to_json(new_document))

# PUT route to update an existing document by ID
@api_documents.route('/documents/<id>', methods=['PUT'])
@token_required
def update_document(id):
    data = request.json
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    
    if result.matched_count:
        updated_document = collection.find_one({"_id": ObjectId(id)})
        return create_response(200, data=bson_to_json(updated_document))
    return create_response(404, message="Document not found")

# DELETE route to delete a document by ID
@api_documents.route('/documents/<id>', methods=['DELETE'])
@token_required
def delete_document(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count:
        return create_response(200, message="Document deleted successfully")
    return create_response(404, message="Document not found")
