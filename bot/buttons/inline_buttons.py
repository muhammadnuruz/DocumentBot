from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons.text import uz_language, ru_language, en_language


async def language_buttons():
    design = [
        [InlineKeyboardButton(text=uz_language, callback_data='language_uz')],
        [InlineKeyboardButton(text=en_language, callback_data='language_en')],
        [InlineKeyboardButton(text=ru_language, callback_data='language_ru')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def admin_yes_or_no_buttons(user_id: int):
    design = [
        [InlineKeyboardButton(text='✅', callback_data=f'yes_or_no_yes_{user_id}'),
         InlineKeyboardButton(text='❌', callback_data=f'yes_or_no_no_{user_id}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)
