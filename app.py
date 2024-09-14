from flask import Flask
from routers.register_routes import register_route

# Create Flask app
app = Flask(__name__)

# Load environment variables (optional if using .env file)
from dotenv import load_dotenv
load_dotenv()

# Import and register API routes
register_route(app)

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
