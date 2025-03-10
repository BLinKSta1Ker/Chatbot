import redis
from pymongo import MongoClient
from app.config import Config

# Connect to Redis
redis_client = redis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True
)

# Connect to MongoDB
mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client["chatbot"]
chat_collection = db["conversations"]