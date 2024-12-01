from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["student_management_system"]

def get_collection(name):
    return db[name]
