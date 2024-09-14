This project is a simple Flask API that interacts with a MongoDB database. It includes endpoints to perform CRUD (Create, Read, Update, Delete) operations on documents in a MongoDB collection.

## Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Docker and Docker Compose::**
   - Make sure Docker is installed on your machine. You can download it from Docker's official website.
   * Install Docker Compose if not already installed. Instructions can be found [here](https://docs.docker.com/engine/install/).

## Environment Variables
Create a .env file in the root of the project directory with the following content:
   ```bash
   cp .env.example .env
   ```

   ```bash
   AZURE_CONNECTION_URI=your_azure_connection_string
   DB_NAME=your_database
   COLLECTION_ID=your_collection
   USERNAME=username
   PASSWORD=password
   ...

   ```

- `AZURE_CONNECTION_URI`: The URI for connecting to the MongoDB container.
* `DB_NAME`: The name of your MongoDB database.
+ `COLLECTION_ID`: The name of your MongoDB collection.
- `USERNAME` & `PASSWORD`: Information to login to get access token

## Running the Application

1. **Ensure Docker is installed and running:**
   - Ensure that both Docker and Docker Compose are installed on your machine and the Docker service is running.


2. **Build and run the containers:**
   In the project root directory, run the following command:
   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```

   This command will:
   - Build the Docker image for the Flask API.
   * Start the Flask API container.

3. **Access the API:**
   Once the containers are up, open your browser or API client and navigate to:
   ```bash
   http://127.0.0.1:5000/api/v1/login
   ```
   Log in to get tokens to access other endpoints in the system. Replace login with other endpoints as needed.
   * Login infomation:
   ```bash
      {
         "username": "phuc",
         "password": "phucnv"
      }
   ```
   - Note: Add the following environment variables to the `.env` file
   ```
   USERNAME=phuc
   PASSWORD='$2b$12$z/OxfOfYiPC3tpepm0LpAO3IBDWRjPhmXp/1OBPIkniVlEtj5dnVe'
   ```

## API Endpoints
- POST `/api/v1/login`: Get access_token to call other endpoints
- GET `/api/v1/documents`: Retrieve all documents from the collection.
* GET `/api/v1/documents/<id>`: Retrieve a specific document by its ObjectId.
+ POST `/api/v1/documents`: Create a new document in the collection. Provide JSON data in the request body.
- PUT `/api/v1/documents/<id>`: Update an existing document by its ObjectId. Provide JSON data in the request body.
+ DELETE `/api/v1/documents/<id>`: Delete a document by its ObjectId.

## Error Handling

If the application fails to connect to MongoDB or if required environment variables are missing, it will raise an appropriate error message. Make sure to set all necessary environment variables and check your MongoDB connection.