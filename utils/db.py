from pymongo import MongoClient
import os

client = MongoClient("mongodb+srv://admin:admin123@cluster0.htt3r.mongodb.net/simulation-ai-engine")  # Use your Mongo URI
db = client["simulation_db"]
templates = db["templates"]
