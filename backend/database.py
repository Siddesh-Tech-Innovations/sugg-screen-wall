import os
from urllib.parse import urlparse
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Get the MongoDB URI from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")

# Raise an error if the URI is not set
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable not set. Please create a .env file and add it.")

# Create the MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)

# Get the database name from the URI path or use a default
db_name = urlparse(MONGODB_URI).path.lstrip('/') or "suggestion_app"

# Get the database object
db = client[db_name]
