from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client

import config

from ..logging import LOGGER
from pymongo import ASCENDING, DESCENDING

# Create a collection object
collection = mongodb["my_collection"]

# Find all documents in the collection, sorted by name in ascending order
results = collection.find().sort("name", ASCENDING)

# Find the first 10 documents in the collection, skipping the first 5
results = collection.find().skip(5).limit(10)

# Find all documents in the collection, projecting only the name and age fields
results = collection.find({}, {"name": 1, "age": 1})

# Find all documents in the collection, with a maximum time limit of 1000ms
results = collection.find().max_time_ms(1000)

TEMP_MONGODB = "mongodb+srv://yash:shivanshudeo@yk.6bvcjqp.mongodb.net/?retryWrites=true&w=majority&appName=yk"


if config.MONGO_DB_URI is None:
    LOGGER(__name__).warning(
        "ɴᴏ ᴍᴏɴɢᴏ  ᴅʙ ᴜʀʟ ғᴏᴜɴᴅ.. sᴏ ɪ ᴡɪʟʟ ᴜsᴇ ᴍʏ ᴏᴡɴᴇʀ's ᴍᴏɴɢᴏ ᴅʙ ᴜʀʟ"
    )
    temp_client = Client(
        "ChampuMusic",
        bot_token=config.BOT_TOKEN,
        api_id=config.API_ID,
        api_hash=config.API_HASH,
    )
    temp_client.start()
    info = temp_client.get_me()
    username = info.username
    temp_client.stop()
    _mongo_async_ = _mongo_client_(TEMP_MONGODB)
    _mongo_sync_ = MongoClient(TEMP_MONGODB)
    mongodb = _mongo_async_[username]
    pymongodb = _mongo_sync_[username]
else:
    _mongo_async_ = _mongo_client_(config.MONGO_DB_URI)
    _mongo_sync_ = MongoClient(config.MONGO_DB_URI)
    mongodb = _mongo_async_.Champu
    pymongodb = _mongo_sync_.Champu