from aiogram.filters import Command, CommandStart
from aiogram import Router, html, types, F 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType
from aiogram.filters import Command
from typing import Any, Dict
from ..keyboards import keyboard
from utils.state import Form
import re
from datetime import datetime, timedelta
registration_router = Router()

phone_pattern = re.compile(r'^\d{10}$')    

@registration_router.message(Form.type_, F.casefold() == "pant")
async def process_pant(message: Message, state:FSMContext):
    try:
        await state.update_data(length=message.text)
        await state.set_state(Form.length)
        await message.answer("Your pant length: ")
    except:
        await message.answer("Some error occurred")

@registration_router.message(Form.type_, F.casefold() == "shirt")
async def process_shirt(message: Message, state:FSMContext):
    try:
        await state.update_data(lenght=message.text)
        await state.set_state(Form.sleeve_length)
        await message.answer("Your sleeve length: ")
    except:
        await message.answer("Some error occurred")


@registration_router.message(Form.phone_number)
async def process_phone(message: Message, state:FSMContext):
    try:
        phone_number = message.text.strip()
        if phone_pattern.match(phone_number):
            await state.update_data(phone_number = message.text)
            await state.set_state(Form.type_)
            await message.answer("What do you want", reply_markup=keyboard.type_request_keyboard)
        else:
            await message.reply("Invalid phone number format. Please enter a 10-digit phone number:") 
    except:
        await message.answer("Some error occurred")

@registration_router.message(Form.length)
async def process_length(message: Message, state:FSMContext):
    # try:
        
    #     await state.update_data(length = message.text)
    #     await state.set_state(Form.hip)
    #     await message.answer("your hip size:")
    # except:
    #     await message.answer("Some error occurred")
    
    try:
        number = int(message.text)  
        if 30 <= number <= 120:
            await state.update_data(length = message.text)
            await state.set_state(Form.hip)
            await message.answer("your hip size:")
        else:
            await message.reply("Please make sure you take the measurement correctly.")
    except ValueError:
        await message.reply("Please enter a valid number.")

@registration_router.message(Form.hip)
async def process_hip(message: Message, state:FSMContext):
    
    try:
        number = int(message.text)  
        if 15 <= number <= 60:
            await state.update_data(hip = message.text)
            await state.set_state(Form.waist)
            await message.answer("your waist size:")
        else:
            await message.reply("Please make sure you take the measurement correctly.")
    except ValueError:
        await message.reply("Please enter a valid number.")

@registration_router.message(Form.waist)
async def process_waist(message: Message, state:FSMContext):
    try:
        number = int(message.text)  
        if 12 <= number <= 50:
            data = await state.update_data(waist = message.text)
            await show_summary(message=message, data=data, state=state)
            await message.answer("see the detail and press confirm button to proceed", reply_markup=keyboard.confirm_or_cancel)
        else:
            await message.reply("Please make sure you take the measurement correctly.")
    except ValueError:
        await message.reply("Please enter a valid number.")

@registration_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    try:
        await state.update_data(name=message.text)
        await state.set_state(Form.phone_number)
        await message.answer(text=f"Nice to meet you {message.text},\nGive us your phone number."
        )
    except:
        await message.answer("Some error occurred")

    

@registration_router.message(Form.sleeve_length)
async def process_sleeve_length(message: Message, state:FSMContext):
    try:
        number = int(message.text)  
        if 12 <= number <= 50:
            await state.update_data(sleeve_length = message.text)
            await state.set_state(Form.body_length)
            await message.answer("your body length:")
        else:
            await message.reply("Please make sure you take the measurement correctly and enter it again.")
    except ValueError:
        await message.reply("Please enter a valid number.")

@registration_router.message(Form.body_length)
async def process_body_length(message: Message, state:FSMContext):
    try:
        number = int(message.text)  
        if 40 <= number <= 100:
            await state.update_data(body_length = message.text)
            await state.set_state(Form.chest_width)
            await message.answer("your chest width:")
        else:
            await message.reply("Please make sure you take the measurement correctly and enter it again.")
    except ValueError:
        await message.reply("Please enter a valid number.")

@registration_router.message(Form.chest_width)
async def process_chest_width(message: Message, state:FSMContext):
    try:
        number = int(message.text)  
        if 30 <= number <= 60:
            data = await state.update_data(chest_width = message.text)
            await show_summary(message=message, data=data, state=state)
            await message.answer("see the detail and press confirm button to proceed", reply_markup=keyboard.confirm_or_cancel)
            
        else:
            await message.reply("Please make sure you take the measurement correctly and enter it again.")
    except ValueError:
        await message.reply("Please enter a valid number.")

async def show_summary(message: Message, data: Dict[str, Any], state: FSMContext) -> None:
    name = data["name"]
    p_number = data["phone_number"]
    preference = data["type_"]
    summary_text = f"Name: {name}\nPhone: {p_number}\nPreference: {preference}"
    two_weeks = timedelta(weeks=2)
    due_date = datetime.today().date() + two_weeks
    await state.update_data(due_date=due_date.strftime("%d/%m/%y"))
    total_length = 0
    if preference == "shirt":
        sl = data["sleeve_length"]
        cw = data["chest_width"]
        bl = data["body_length"]
        total_length = int(sl) + int(cw) + int(bl)
        summary_text += f"\nSleeve Length: {sl}"
        summary_text += f"\nChest Width: {cw}"
        summary_text += f"\nBody Length: {bl}"
    if preference == "pant":
        l = data["length"]
        w = data["waist"]
        h = data["hip"]
        total_length = int(l) + int(w) + int(h)
        summary_text += f"\nLength: {l}"
        summary_text += f"\nWaist: {w}"
        summary_text += f"\nHip: {h}"
    price = total_length * 30 + 1200
    await state.update_data(price=price)
    summary_text += f"\nPrice: {price}\nDue date: {due_date}"
    await message.answer(text=summary_text)