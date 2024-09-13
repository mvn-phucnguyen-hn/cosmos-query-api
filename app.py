import os
from flask import Flask
from pymongo import MongoClient
from api import register_routes

# Create Flask app
app = Flask(__name__)

# Load environment variables (optional if using .env file)
from dotenv import load_dotenv
load_dotenv()

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

# Store the MongoDB collection in the app config
app.config['collection'] = collection

# Import and register API routes
register_routes(app)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
