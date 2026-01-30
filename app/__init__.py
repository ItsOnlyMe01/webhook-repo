from flask import Flask
from app.webhook.routes import webhook
from app.extensions import mongo  # Import the mongo object

# Creating our flask app
def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"
    
    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
