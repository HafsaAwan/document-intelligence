import os
from dotenv import load_dotenv

# Find the .env file in the 'backend' directory
# __file__ is the current file's path: backend/app/core/config.py
# os.path.dirname(...) gets the directory: backend/app/core
# os.path.dirname(os.path.dirname(...)) goes up one level: backend/app
# os.path.dirname(os.path.dirname(os.path.dirname(...))) goes up another level: backend/
# Then we join that path with '.env'
DOTENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')

# Load the .env file
load_dotenv(DOTENV_PATH)

# Now, we can safely access the API key as an environment variable
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Simple check to make sure the key was loaded
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY not found. Make sure it's set in your .env file.")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Make sure it's set in your .env file.")