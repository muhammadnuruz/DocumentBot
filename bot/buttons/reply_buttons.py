import json
from email.policy import default

import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.text import back_main_menu, choice_language, choice_language_ru, choice_language_en, back_main_menu_ru, \
    back_main_menu_en, none_advert, forward_advert, adverts, math, science, develop, math_en, science_en, develop_en, \
    develop_ru, science_ru, math_ru


async def main_menu_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    categories = json.loads(requests.get(url="http://127.0.0.1:8000/api/documents/").content)
    design = []
    if tg_user['language'] == 'uz':
        for category in categories['results']:
            design.append([category['name']])
        # design.append([math])
        # design.append([science])
        # design.append([develop])
        design.append([choice_language])

    elif tg_user['language'] == 'en':
        for category in categories['results']:
            design.append([category['en_name']])
        # design.append([math_en])
        # design.append([science_en])
        # design.append([develop_en])
        design.append([choice_language_en])
    else:
        for category in categories['results']:
            design.append([category['ru_name']])
        # design.append([math_ru])
        # design.append([science_ru])
        # design.append([develop_ru])
        design.append([choice_language_ru])
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu_button(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [[back_main_menu]]
    elif tg_user['language'] == 'en':
        design = [[back_main_menu_en]]
    else:
        design = [[back_main_menu_ru]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_menu_buttons():
    design = [
        [adverts],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def advert_menu_buttons():
    design = [
        [none_advert, forward_advert],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


def phone_number_request_button():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text="📱 Telefon raqamni ulashish", request_contact=True)
    keyboard.add(button)
    return keyboard


async def yes_or_no_button():
    design = [
        ['✅', '❌']
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
