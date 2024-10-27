import json

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import language_buttons
from bot.buttons.reply_buttons import main_menu_buttons, phone_number_request_button
from bot.buttons.text import back_main_menu, choice_language, choice_language_en, choice_language_ru
from bot.dispatcher import dp, bot
from main import admins


async def get_user_language(user_id):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{user_id}/").content)
    try:
        return tg_user['language'] if tg_user else 'uz'
    except KeyError:
        return 'uz'


@dp.message_handler(commands=['start'])
async def start_function(msg: types.Message, state: FSMContext):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    user_language = await get_user_language(msg.from_user.id)
    try:
        if tg_user['detail']:
            await state.set_state('language_1')
            await msg.answer(text="""
Tilni tanlang

-------------

Select a language

-------------

Выберите язык""", reply_markup=await language_buttons())
    except KeyError:
        if user_language == 'uz':
            await msg.answer(text=f"Bot yangilandi hurmatli {tg_user['full_name']}",
                             reply_markup=await main_menu_buttons(msg.from_user.id))
        elif user_language == 'en':
            await msg.answer(text=f"Bot updated dear {tg_user['full_name']}",
                             reply_markup=await main_menu_buttons(msg.from_user.id))
        else:
            await msg.answer(text=f"Бот обновлён, дорогой {tg_user['full_name']}",
                             reply_markup=await main_menu_buttons(msg.from_user.id))



@dp.callback_query_handler(Text(startswith='language_'), state='language_1')
async def language_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        data['language'] = call.data.split('_')[-1]

    await state.set_state('name')
    language_texts = {
        'uz': "Iltimos, ismingizni kiriting:",
        'en': "Please enter your name:",
        'ru': "Пожалуйста, введите ваше имя:"
    }
    await call.message.answer(language_texts[data['language']])


@dp.message_handler(state='name')
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await state.set_state('phone_number')
    language_texts = {
        'uz': "Iltimos, telefon raqamingizni ulashing:",
        'en': "Please share your phone number:",
        'ru': "Пожалуйста, поделитесь своим номером телефона:"
    }
    await message.answer(language_texts[data['language']], reply_markup=phone_number_request_button())


@dp.message_handler(content_types=types.ContentType.CONTACT, state='phone_number')
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
    post_data = {
        "chat_id": str(message.from_user.id),
        "full_name": data['name'],
        "username": message.from_user.username,
        "language": data['language'],
        "phone_number": data['phone_number']
    }
    requests.post(url=f"http://127.0.0.1:8000/api/telegram-users/create/", data=post_data)
    user_language = data['language']
    welcome_texts = {
        'uz': "Hush kelibsiz 😊",
        'en': "Welcome 😊",
        'ru': "Добро пожаловать 😊"
    }
    await message.answer(text=welcome_texts[user_language], reply_markup=await main_menu_buttons(message.from_user.id))

    for admin in admins:
        await bot.send_message(chat_id=admin, text=f"""
Yangi user🆕
ID: <a href='tg://user?id={message.from_user.id}'>{message.from_user.id}</a>
Username: @{message.from_user.username}
Ism-Familiya: {data['name']}
Telefon-raqam: {data['phone_number']}""", parse_mode='HTML')
    await state.finish()


@dp.message_handler(Text(back_main_menu), state='*')
async def back_main_menu_function(msg: types.Message, state: FSMContext):
    user_language = await get_user_language(msg.from_user.id)
    greeting_text = {
        'uz': f"Assalomu alaykum {msg.from_user.first_name}",
        'en': f"Hello {msg.from_user.first_name}",
        'ru': f"Здравствуйте {msg.from_user.first_name}"
    }.get(user_language, f"Assalomu alaykum {msg.from_user.first_name}")

    await msg.answer(text=greeting_text, reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()


@dp.callback_query_handler(Text(back_main_menu), state='*')
async def back_main_menu_function(call: types.CallbackQuery, state: FSMContext):
    user_language = await get_user_language(call.from_user.id)
    greeting_text = {
        'uz': f"Assalomu alaykum {call.from_user.first_name}",
        'en': f"Hello {call.from_user.first_name}",
        'ru': f"Здравствуйте {call.from_user.first_name}"
    }.get(user_language, f"Assalomu alaykum {call.from_user.first_name}")

    await call.message.delete()
    await call.message.answer(text=greeting_text, reply_markup=await main_menu_buttons(call.from_user.id))
    await state.finish()


@dp.message_handler(Text(equals=[choice_language, choice_language_en, choice_language_ru]))
async def change_language_function_1(msg: types.Message):
    await msg.answer(text="""
Tilni tanlang

-------------

Select a language

-------------

Выберите язык""", reply_markup=await language_buttons())


@dp.callback_query_handler(Text(startswith='language_'))
async def language_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content)
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "language": call.data.split("_")[-1]
    }
    requests.patch(url=f"http://127.0.0.1:8000/api/telegram-users/update/{tg_user['id']}/", data=data)
    await call.message.delete()
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text="Til o'zgartirildi 🇺🇿", reply_markup=await main_menu_buttons(call.from_user.id))
    elif call.data.split("_")[-1] == 'en':
        await call.message.answer(text="The Language updated 🇺🇿",
                                  reply_markup=await main_menu_buttons(call.from_user.id))
    else:
        await call.message.answer(text="Язык изменен 🇷🇺", reply_markup=await main_menu_buttons(call.from_user.id))
