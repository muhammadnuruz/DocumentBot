import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from bot.buttons.inline_buttons import admin_yes_or_no_buttons
from bot.buttons.reply_buttons import back_main_menu_button, yes_or_no_button, main_menu_buttons
from bot.buttons.text import math, math_ru, math_en, science, science_en, science_ru, develop, develop_ru, develop_en
from bot.dispatcher import dp, bot
from bot.handlers import get_user_language
from main import admins


# @dp.message_handler(
#     Text(equals=[math, math_ru, math_en, science, science_en, science_ru, develop, develop_ru, develop_en]))
# async def sciences_function(msg: types.Message):
#     language = await get_user_language(msg.from_user.id)
#     if language == 'uz':
#         await msg.answer(text="""
# Buyurtma tasdiqlandi.
#
# Buyurtmangiz 50% to’lov qilganingizdan keyin boshlanadi va 24 soat
# ichida tayyorlab beriladi!
#
# Ko’proq ma’lumot uchun:
# @prezintatsiyauz_admin
# @preuzadmin
#
# Kanal: https://t.me/preuzb
# Natijalar: @pre_ishonch
# Asoschi va bosh direktor: @MUKHAMMADSODlQ""")
#     elif language == 'en':
#         await msg.answer("""
# Заказ подтвержден.
#
# Ваш заказ начинается после оплаты 50% и 24 часов.
# приготовлено внутри!
#
# Для получения дополнительной информации:
# @prezintatsiyauz_admin
# @preuzadmin
#
# Канал: https://t.me/preuzb
# Результаты: @pre_ishonch
# Основатель и генеральный директор: @MUKHAMMADSODlQ
# """)
#     else:
#         await msg.answer("""
# Order confirmed.
#
# Your order starts after you pay 50% and 24 hours
# prepared inside!
#
# For more information:
# @prezintatsiyauz_admin
# @preuzadmin
#
# Channel: https://t.me/preuzb
# Results: @pre_ishonch
# Founder and CEO: @MUKHAMMADSODlQ""")
#     tg_user = json.loads(
#         requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
#     for i in admins:
#         try:
#             await bot.send_message(chat_id=i, text=f"""
# ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
# Ism-Familiya: {tg_user['full_name']}
# Username: @{msg.from_user.username}
# Telefon-raqam: {tg_user['phone_number']}
# Prezentatsiya turi: {msg.text}
#
#
# Shaxsiydan chatda aloqaga chiqing!""", parse_mode="HTML")
#         except Exception:
#             pass


@dp.message_handler()
async def order_function(msg: types.Message, state: FSMContext):
    categories = json.loads(requests.get(url="http://127.0.0.1:8000/api/documents/").content)['results']
    for category in categories:
        if msg.text == category['name'] or msg.text == category['ru_name'] or msg.text == category['en_name']:
            async with state.proxy() as data:
                data['name'] = msg.text
                data['price'] = category['price']
            await state.set_state('page_number')
            language = await get_user_language(msg.from_user.id)
            if language == 'uz':
                await msg.answer(f"""
Siz {msg.text} ta’rif rejasinitanladingiz. Endi necha sahifali slayd kerakligini raqamlar orqali kiriting. (Masalan 10, 15, 18 va h.k.)

{msg.text} 1 sahifa uchun {data['price']} uzs!""",
                                 reply_markup=await back_main_menu_button(msg.from_user.id))
            elif language == 'en':
                await msg.answer(f"""
You have selected the description plan {msg.text}. Now enter how many page slides you need by numbers. (For example 10, 15, 18, etc.)

{msg.text} {data['price']} uzs for 1 page!""",
                                 reply_markup=await back_main_menu_button(msg.from_user.id))
            else:
                await msg.answer(f"""
Вы выбрали план описания {msg.text}. Теперь введите числом необходимое количество слайдов страниц. (Например, 10, 15, 18 и т. д.)

{msg.text} {data['price']} узе за 1 страницу!""",
                                 reply_markup=await back_main_menu_button(msg.from_user.id))
            return


@dp.message_handler(state='page_number')
async def order_function_2(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['page_number'] = int(msg.text)
    except ValueError:
        await state.set_state('page_number')
        lang = await get_user_language(msg.from_user.id)
        if lang == 'uz':
            await msg.answer(f"""Faqatgina sonlardan foydalaning!\n\n (Masalan 10, 15, 18 va h.k.)""",
                             reply_markup=await back_main_menu_button(msg.from_user.id))
        elif lang == 'en':
            await msg.answer(f"""Use numbers only!\n\n(For example 10, 15, 18, etc.)""",
                             reply_markup=await back_main_menu_button(msg.from_user.id))
        else:
            await msg.answer(f"""Используйте только цифры!\n\n (например, 10, 15, 18 и т. д.)""",
                             reply_markup=await back_main_menu_button(msg.from_user.id))
        return
    await state.set_state('paragraph_name')
    lang = await get_user_language(msg.from_user.id)
    if lang == 'uz':
        await msg.answer(f"""Endi esa mavzu nomini to’liq yozib qoldiring.\n(Masalan: “Alisher Navoiy”)""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    elif lang == 'en':
        await msg.answer(f"""Now write the full name of the topic.\n(For example: "Alisher Navoi")""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))
    else:
        await msg.answer(f"""Теперь напишите полное название темы.\n(Например: «Алишер Навои»)""",
                         reply_markup=await back_main_menu_button(msg.from_user.id))


@dp.message_handler(state='paragraph_name')
async def order_function_3(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['paragraph_name'] = msg.text
    price = data['page_number'] * data['price']
    lang = await get_user_language(msg.from_user.id)
    await state.set_state('yes_or_no')
    if lang == 'uz':
        await msg.answer(f"""
Siz {data['name']} ta’rif rejasida
{data['paragraph_name']} mavzusida {data['page_number']} sahifadan iborat prezintatsiya buyurtma qildingiz. 
Buyurtma narxi {price} 
 
Buyurtmani tasdiqlaysizmi?""",
                         reply_markup=await yes_or_no_button())
    elif lang == 'en':
        await msg.answer(f"""
You are in the {data['name']} definition plan
You have ordered a presentation consisting of {data['page_number']} pages on {data['paragraph_name']}. 
Order price {price} 
 
Confirm the order?""",
                         reply_markup=await yes_or_no_button())
    else:
        await msg.answer(f"""
Вы находитесь в плане определения {data['name']}
Вы заказали презентацию, состоящую из {data['page_number']} страниц на сайте {data['paragraph_name']}. 
Стоимость заказа {price} 
 
Подтвердить заказ?""",
                         reply_markup=await yes_or_no_button())


# Define messages for each language
MESSAGES = {
    'uz': {
        'order_confirmed': """
Buyurtma tasdiqlandi.
Buyurtmangiz 50% to’lov qilganingizdan keyin boshlanadi va 24 soat ichida tayyorlab beriladi!
Ko’proq ma’lumot uchun:
@prezintatsiyauz_admin
@preuzadmin

Kanal: https://t.me/preuzb
Natijalar: @pre_ishonch
Asoschi va bosh direktor: @MUKHAMMADSODlQ

Donat uchun: 6262730036434050
""",
        'order_cancelled': "Buyurtma bekor qilindi",
        'order_rejected': """
Sizning buyurtmangiz admin tomonidan bekor qilindi❌

Ko’proq ma’lumot uchun:
@prezintatsiyauz_admin
@preuzadmin
Asoschi va bosh direktor: @MUKHAMMADSODlQ
"""
    },
    'ru': {
        'order_confirmed': """
Заказ подтвержден.
Ваш заказ начнется после оплаты 50% и будет готов в течение 24 часов!
Для получения дополнительной информации:
@prezintatsiyauz_admin
@preuzadmin

Канал: https://t.me/preuzb
Результаты: @pre_ishonch
Основатель и генеральный директор: @MUKHAMMADSODlQ

Для доната: 6262730036434050
""",
        'order_cancelled': "Заказ отменен",
        'order_rejected': """
Ваш заказ был отклонен администратором❌

Для получения дополнительной информации:
@prezintatsiyauz_admin
@preuzadmin
Основатель и генеральный директор: @MUKHAMMADSODlQ
"""
    },
    'en': {
        'order_confirmed': """
Order confirmed.
Your order will begin after 50% payment and will be ready within 24 hours!
For more information:
@prezintatsiyauz_admin
@preuzadmin

Channel: https://t.me/preuzb
Results: @pre_ishonch
Founder and CEO: @MUKHAMMADSODlQ

To donate: 6262730036434050
""",
        'order_cancelled': "Order cancelled",
        'order_rejected': """
Your order has been cancelled by the admin❌

For more information:
@prezintatsiyauz_admin
@preuzadmin
Founder and CEO: @MUKHAMMADSODlQ
"""
    }
}


@dp.message_handler(state='yes_or_no')
async def order_function_4(msg: types.Message, state: FSMContext):
    # Fetch user language from TelegramUsers
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    user_lang = tg_user.get('language', 'uz')  # default to Uzbek if language not set

    if msg.text == '✅':
        await msg.answer(text=MESSAGES[user_lang]['order_confirmed'],
                         reply_markup=await main_menu_buttons(msg.from_user.id))

        # Admin notification
        async with state.proxy() as data:
            pass
        post_data = {
            'chat_id': msg.from_user.id,
            'name': data['name'],
            'page_number': data['page_number'],
            'price': data['page_number'] * data['price'],
            'paragraph_name': data['paragraph_name'],
        }
        requests.post(url=f"http://127.0.0.1:8000/api/analyses/create/", data=post_data)
        for i in admins:
            try:
                await bot.send_message(chat_id=i, text=f"""
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Ism-Familiya: {tg_user['full_name']}
Username: @{msg.from_user.username}
Telefon-raqam: {tg_user['phone_number']}
Prezentatsiya turi: {data['name']}
Prezentatsiya Mavzusi: {data['paragraph_name']}
Sahifalar soni: {data['page_number']}
1 sahifa uchun narx: {data['price']}
Umumiy narxi: {data['page_number'] * data['price']}
""", reply_markup=await admin_yes_or_no_buttons(msg.from_user.id), parse_mode="HTML")
            except Exception:
                pass
        await state.finish()
    else:
        await state.finish()
        await msg.answer(text=MESSAGES[user_lang]['order_cancelled'],
                         reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(startswith='yes_or_no_'))
async def order_function_5(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.data.split("_")[-1]
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    user_lang = tg_user.get('language', 'uz')

    response = call.data.split("_")[-2]
    if response == 'yes':
        async with state.proxy() as data:
            data['chat_id'] = chat_id
        await state.set_state('get_file')
        await call.message.answer(text="Faylin yuboring:",
                                  reply_markup=await back_main_menu_button(call.from_user.id))
    else:
        await call.answer("Buyurtma bekor qilindi❌", show_alert=True)
        await state.finish()
        try:
            await bot.send_message(chat_id=chat_id, text=MESSAGES[user_lang]['order_rejected'])
        except Exception as e:
            pass


@dp.message_handler(state='get_file', content_types=ContentType.DOCUMENT)
async def handle_file_upload(msg: types.Message, state: FSMContext):
    file_id = msg.document.file_id

    async with state.proxy() as data:
        data['file_id'] = file_id
    await state.set_state('finish')
    await msg.answer("Fayl qabul qilindi, yuborishga tayyormisiz?")


@dp.message_handler(lambda message: message.text.lower() == 'ha', state='finish')
async def confirm_and_send_file(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        file_id = data['file_id']
    try:
        await bot.send_document(chat_id=data['chat_id'], document=file_id)
        await msg.answer("Fayl yuborildi!")
    except Exception as e:
        await msg.answer(text="Fayl userga yuborilmadi!\n\nShaxsiy chatdan yuboring!")
        await bot.send_message(chat_id=admins[0], text=e)
    await state.finish()
