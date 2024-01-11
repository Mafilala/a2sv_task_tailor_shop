
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

type_request_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        
           [ InlineKeyboardButton(text="Pant", callback_data="pant"),
            InlineKeyboardButton(text="Shirt", callback_data="shirt")]
    ]
)

see_more_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="See more..", callback_data='more_info')],
        ])

first_reply_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        
           [ InlineKeyboardButton(text="👋 Register!", callback_data="register"),
            InlineKeyboardButton(text="Explore our shop", callback_data="explore")]
    ]
)

confirm_or_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        
           [ InlineKeyboardButton(text="Confirm", callback_data="confirm"),
            InlineKeyboardButton(text="Cancel", callback_data="cancel")]
    ]
)
