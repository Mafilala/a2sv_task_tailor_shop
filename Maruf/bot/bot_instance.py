import os
from aiogram import Bot

# Use the commented code below if you store the token api in .env
from dotenv import load_dotenv
load_dotenv()
TOKEN_API = os.environ.get("TOKEN_API")
print(TOKEN_API)
from aiogram.client.session.aiohttp import AiohttpSession
bot = Bot(
    token=TOKEN_API,
    parse_mode='HTML',
    session=AiohttpSession(proxy='http://proxy.server:3128')
)

# bot = Bot(
#     token=TOKEN_API,
#     parse_mode='HTML'
# )