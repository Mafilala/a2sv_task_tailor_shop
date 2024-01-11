from aiogram.filters import Command
from aiogram import Router, types 
from aiogram.methods.send_photo import SendPhoto
from utils.state import Form
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType
from bot.bot_instance import bot
from aiogram.utils.media_group import MediaGroupBuilder
from utils.categories import categories
callback_router = Router()
from ..keyboards import keyboard
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from pymongo.mongo_client import MongoClient
import os
from ..database.services.order_services import create_order
import uuid
@callback_router.callback_query(lambda c: c.data.startswith("register"))
async def process_registration(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await state.set_state(Form.name)
        await callback_query.message.answer("Hello Welcome to  our tailor shop, Tell us your name: ")
    except:
        await callback_query.answer("Some error occurred")


@callback_router.callback_query(lambda c: c.data.startswith("pant"))
async def process_pant(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.edit_message_reply_markup(callback_query.message.chat.id,callback_query.message.message_id,reply_markup=None)
        await state.update_data(type_="pant")
        await state.set_state(Form.length)
        await callback_query.message.answer("your pant length: ")
    except:
        await callback_query.answer("Some error occurred")

@callback_router.callback_query(lambda c: c.data.startswith("shirt"))
async def process_shirt(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.edit_message_reply_markup(callback_query.message.chat.id,callback_query.message.message_id,reply_markup=None)
        await state.update_data(type_="shirt")
        await state.set_state(Form.sleeve_length)
        await callback_query.message.answer("your shirt sleeve length: ")
    except:
        await callback_query.answer("Some error occurred")



@callback_router.callback_query(lambda c: c.data.startswith("explore"))
async def handle_explore(callback_query: types.CallbackQuery):
    async def send_photo_grid(chat_id, categories):
        for category, urls in categories.items():
            media_group = MediaGroupBuilder(caption=f"{category}")
            text = f"<b><i>\n\n                                  {category}</i></b>"
            await callback_query.message.answer(text, parse_mode="HTML")
            for idx, url in enumerate(urls):
                if idx == 2:
                    break
                # await bot(SendPhoto(chat_id=chat_id, photo=url))

                # Add photo
                media_group.add_photo(media=url)
            await bot.send_media_group(chat_id=chat_id, media=media_group.build())
        
            await callback_query.message.answer(
        f"click 'see more' button for more {category}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="See more..", callback_data=f'more_{category}')],
        ])
    )

            
    
    async def explore_photos_callback(callback_query: types.CallbackQuery):
        await callback_query.answer()  # Acknowledge (if needed)
        user_id = callback_query.from_user.id
        
        await send_photo_grid(user_id, categories)

    await explore_photos_callback(callback_query)

@callback_router.callback_query(lambda c: c.data.startswith("more"))
async def process_see_more(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        key = callback_query.data.split("_")[-1]
        urls = categories[key]
        media_group = MediaGroupBuilder(caption=f"{key}")
        text = f"<b><i>\n\n                                  {key}</i></b>"
        await callback_query.message.answer(text, parse_mode="HTML")
        for url in urls:
            # await bot(SendPhoto(chat_id=chat_id, photo=url))

            # Add photo
            media_group.add_photo(media=url)
        await bot.send_media_group(chat_id=callback_query.from_user.id, media=media_group.build())
        
    except:
        await callback_query.answer("Some error occurred")

@callback_router.callback_query(lambda c: c.data.startswith("confirm"))
async def process_registration(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.edit_message_reply_markup(callback_query.message.chat.id,callback_query.message.message_id,reply_markup=None)
        data = await state.get_data()
        id = uuid.uuid4()
        await create_order(_id=str(id), **data)
        reply_text = "___Thanks for confirming___"
        await callback_query.message.answer(reply_text, parse_mode="Markdown")
    except Exception as e:
        await callback_query.answer("Some error occurred", e)

@callback_router.callback_query(lambda c: c.data.startswith("cancel"))
async def process_registration(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.edit_message_reply_markup(callback_query.message.chat.id,callback_query.message.message_id,reply_markup=None)
        reply_text = "___your order is cancelled___"
        await callback_query.message.answer(reply_text, parse_mode="Markdown")
    except:
        await callback_query.answer("Some error occurred")