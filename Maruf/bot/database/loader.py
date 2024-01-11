from aiogram import Bot, Dispatcher
import certifi
from pymongo.mongo_client import MongoClient

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
load_dotenv()
uri = os.environ.get("uri")


cluster = MongoClient(uri, tlsCAFile=certifi.where())
db = cluster["tailor_shop_db"]
collection = db["orders"]
