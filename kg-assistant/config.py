
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_DEFAULT_MODEL = os.getenv("LLM_DEFAULT_MODEL")

if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
    print("⚠️ Missing Neo4j config. Check your .env file!")

if not all([LLM_BASE_URL, DSX_API_KEY, LLM_DEFAULT_MODEL]):
    print("⚠️ Missing LLM config. Check your .env file!")
