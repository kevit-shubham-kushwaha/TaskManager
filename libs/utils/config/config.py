import os 

import dotenv

dotenv.load_dotenv(".env")

MONGODB_URI = os.getenv("MONGODB_URI")
YOUR_SECRET_KEY = os.getenv("SECRET_KEY")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")