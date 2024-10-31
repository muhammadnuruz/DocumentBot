import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from bot.buttons.inline_buttons import admin_yes_or_no_buttons
from bot.buttons.reply_buttons import back_main_menu_button, yes_or_no_button, main_menu_buttons
from bot.buttons.text import ui, ui_ru, ui_en, web, web_en, web_ru
from bot.dispatcher import dp, bot
from bot.handlers import get_user_language
from main import admins


# @dp.message_handler(
#     Text(equals=[ui, ui_ru, ui_en, web, web_en, web_ru]))
# async def webs_function(msg: types.Message):
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
# Buyurtma turi: {msg.text}
#
#
# Shaxsiydan chatda aloqaga chiqing!""", parse_mode="HTML")
#         except Exception:
#             pass


@dp.message_handler(Text(equals=["Taklifnoma(QR-kodli)", "Приглашение (с QR-кодом)", "Invitation (with QR code)"]))
async def invitation_request(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if language == 'uz':
        await msg.answer("""
Taklifnoma uchun kerakli ma'lumotlarni ketma-ketlikda yuboring:
Kelin-kuyov ismi, familiyasi.
To'y sanasi.
Manzil.
To'yxona nomi.
""")
    elif language == 'ru':
        await msg.answer("""
Для приглашения отправьте данные в следующем порядке:
Имя и фамилия жениха и невесты.
Дата свадьбы.
Адрес.
Название зала.
""")
    else:  # English
        await msg.answer("""
For the invitation, send the necessary information in the following order:
Bride and groom's name and surname.
Wedding date.
Address.
Hall name.
""")
    await state.set_state("waiting_for_invitation_info")


@dp.message_handler(state="waiting_for_invitation_info")
async def collect_invitation_info(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if language == 'uz':
        await msg.answer(text="""
Buyurtma tasdiqlandi.

Buyurtmangiz 50% to’lov qilganingizdan keyin boshlanadi va 24 soat
ichida tayyorlab beriladi!

Ko’proq ma’lumot uchun:
@prezintatsiyauz_admin
@preuzadmin

Kanal: https://t.me/preuzb
Natijalar: @pre_ishonch
Asoschi va bosh direktor: @MUKHAMMADSODlQ""")
    elif language == 'en':
        await msg.answer("""
Заказ подтвержден.

Ваш заказ начинается после оплаты 50% и 24 часов.
приготовлено внутри!

Для получения дополнительной информации:
@prezintatsiyauz_admin
@preuzadmin

Канал: https://t.me/preuzb
Результаты: @pre_ishonch
Основатель и генеральный директор: @MUKHAMMADSODlQ
""")
    else:
        await msg.answer("""
Order confirmed.

Your order starts after you pay 50% and 24 hours
prepared inside!

For more information:
@prezintatsiyauz_admin
@preuzadmin

Channel: https://t.me/preuzb
Results: @pre_ishonch
Founder and CEO: @MUKHAMMADSODlQ""")
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    for admin_id in admins:
        text = {
            'uz': f"Taklifnoma ma'lumotlari:\n{msg.text}",
            'ru': f"Данные для приглашения:\n{msg.text}",
            'en': f"Invitation details:\n{msg.text}"
        }.get(language, msg.text)

        try:
            await bot.send_message(chat_id=admin_id, text=f"""
{text}
Foydalanuvchi ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Ism: {tg_user['full_name']}
Username: @{msg.from_user.username}
Telefon-raqam: {tg_user['phone_number']}
""", parse_mode="HTML")
        except Exception:
            pass
    await state.finish()


# Rezyume uchun so'rov va adminlarga yuborish
@dp.message_handler(Text(equals=["Rezyume", "Резюме", "Resume"]))
async def resume_request(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if language == 'uz':
        await msg.answer("""
Rezyume uchun, quyidagi ma'lumotlarni yuboring:
Ism-familiya, otasini ismi,
Tug'ilgan yili,
Tug'ilgan joyi,
O'qish joylari (boshlagan va tugatgan yillari),
Ish faoliyati,
Partiyadorligi,
Email va telefon raqami.
""")
    elif language == 'ru':
        await msg.answer("""
Для резюме отправьте следующие данные:
Имя и фамилия, отчество,
Дата рождения,
Место рождения,
Учебные заведения (годы начала и окончания),
Трудовая деятельность,
Членство в партии,
Электронная почта и телефонный номер.
""")
    else:  # English
        await msg.answer("""
For the resume, send the following information:
Name and surname, father's name,
Date of birth,
Place of birth,
Educational institutions (start and end years),
Work experience,
Party membership,
Email and phone number.
""")
    await state.set_state("waiting_for_resume_info")


@dp.message_handler(state="waiting_for_resume_info")
async def collect_resume_info(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if language == 'uz':
        await msg.answer(text="""
Buyurtma tasdiqlandi.

Buyurtmangiz 50% to’lov qilganingizdan keyin boshlanadi va 24 soat
ichida tayyorlab beriladi!

Ko’proq ma’lumot uchun:
@prezintatsiyauz_admin
@preuzadmin

Kanal: https://t.me/preuzb
Natijalar: @pre_ishonch
Asoschi va bosh direktor: @MUKHAMMADSODlQ""")
    elif language == 'en':
        await msg.answer("""
Заказ подтвержден.

Ваш заказ начинается после оплаты 50% и 24 часов.
приготовлено внутри!

Для получения дополнительной информации:
@prezintatsiyauz_admin
@preuzadmin

Канал: https://t.me/preuzb
Результаты: @pre_ishonch
Основатель и генеральный директор: @MUKHAMMADSODlQ
    """)
    else:
        await msg.answer("""
Order confirmed.

Your order starts after you pay 50% and 24 hours
prepared inside!

For more information:
@prezintatsiyauz_admin
@preuzadmin

Channel: https://t.me/preuzb
Results: @pre_ishonch
Founder and CEO: @MUKHAMMADSODlQ""")
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    for admin_id in admins:
        text = {
            'uz': f"Rezyume ma'lumotlari:\n{msg.text}",
            'ru': f"Данные для резюме:\n{msg.text}",
            'en': f"Resume details:\n{msg.text}"
        }.get(language, msg.text)

        try:
            await bot.send_message(chat_id=admin_id, text=f"""
{text}
Foydalanuvchi ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Ism: {tg_user['full_name']}
Username: @{msg.from_user.username}
Telefon-raqam: {tg_user['phone_number']}
""", parse_mode="HTML")
        except Exception:
            pass
    await state.finish()


@dp.message_handler(Text(equals=["YouTube uchun banner", "Баннер для YouTube", "Banner for YouTube"]))
async def youtube_request(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if language == 'uz':
        await msg.answer("""
YouTube kanali uchun kerakli ma'lumotlarni yuboring:
1. Kanal nomi.
2. Kanalni nima haqida yuritilishini.
""")
    elif language == 'ru':
        await msg.answer("""
Отправьте необходимые данные для канала YouTube:
1. Название канала.
2. О чем будет канал.
""")
    else:  # English
        await msg.answer("""
Please send the necessary information for your YouTube channel:
1. Channel name.
2. What the channel will be about.
""")
    await state.set_state("waiting_for_youtube_info")


@dp.message_handler(state="waiting_for_youtube_info")
async def collect_youtube_info(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)

    channel_info = msg.text

    if language == 'uz':
        await msg.answer(text="YouTube uchun ma'lumotlar qabul qilindi.")
    elif language == 'ru':
        await msg.answer(text="Данные для YouTube приняты.")
    else:
        await msg.answer(text="YouTube information received.")

    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    for admin_id in admins:
        text = {
            'uz': f"YouTube kanal ma'lumotlari:\n{channel_info}",
            'ru': f"Данные канала YouTube:\n{channel_info}",
            'en': f"YouTube channel details:\n{channel_info}"
        }.get(language, channel_info)

        try:
            await bot.send_message(chat_id=admin_id, text=f"""
{text}
Foydalanuvchi ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Ism: {tg_user['full_name']}
Username: @{msg.from_user.username}
Telefon-raqam: {tg_user['phone_number']}
""", parse_mode="HTML")
        except Exception:
            pass
    await state.finish()


# Logo uchun ma'lumotlarni so'rash
@dp.message_handler(Text(equals=["Logo tayyorlash", "Подготовка логотипа", "Logo preparation"]))
async def logo_request(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if language == 'uz':
        await msg.answer("""
Logo uchun kerakli ma'lumotlarni yuboring:
1. Kompaniya nomi.
2. Nima ish bilan shug'ullanadi.
""")
    elif language == 'ru':
        await msg.answer("""
Отправьте необходимые данные для логотипа:
1. Название компании.
2. Чем она занимается.
""")
    else:  # English
        await msg.answer("""
Please send the necessary information for the logo:
1. Company name.
2. What it does.
""")
    await state.set_state("waiting_for_logo_info")


@dp.message_handler(state="waiting_for_logo_info")
async def collect_logo_info(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)

    logo_info = msg.text

    if language == 'uz':
        await msg.answer(text="Logo uchun ma'lumotlar qabul qilindi.")
    elif language == 'ru':
        await msg.answer(text="Данные для логотипа приняты.")
    else:
        await msg.answer(text="Logo information received.")

    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    for admin_id in admins:
        text = {
            'uz': f"Logo ma'lumotlari:\n{logo_info}",
            'ru': f"Данные логотипа:\n{logo_info}",
            'en': f"Logo details:\n{logo_info}"
        }.get(language, logo_info)

        try:
            await bot.send_message(chat_id=admin_id, text=f"""
    {text}
    Foydalanuvchi ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
    Ism: {tg_user['full_name']}
    Username: @{msg.from_user.username}
    Telefon-raqam: {tg_user['phone_number']}
    """, parse_mode="HTML")
        except Exception as e:
            print(f"Error sending message to admin: {e}")  # Log the error for debugging
    await state.finish()


@dp.message_handler(Text(equals=["Tarjimonlik xizmati", "Услуги перевода", "Translation service"]))
async def translation_request(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if language == 'uz':
        await msg.answer("""
Tarjima qilish uchun quyidagi ma'lumotlarni yuboring:
1. Tarjima qilinishi kerak bo'lgan matn.
2. Skrinshot (rasm) yuborish mumkin.
""")
    elif language == 'ru':
        await msg.answer("""
Отправьте информацию для перевода:
1. Текст, который нужно перевести.
2. Можно отправить скриншот (изображение).
""")
    else:  # English
        await msg.answer("""
Please send the information to be translated:
1. The text that needs to be translated.
2. A screenshot (image) can be sent.
""")
    await state.set_state("waiting_for_translation_info")


@dp.message_handler(state="waiting_for_translation_info", content_types=types.ContentTypes.ANY)
async def collect_translation_info(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)

    if msg.content_type == "text":
        translation_info = msg.text
    elif msg.content_type == "photo":
        translation_info = "Skrinshot qabul qilindi."  # Skrinshot qabul qilindi
    else:
        await msg.answer("Iltimos, faqat matn yoki skrinshot yuboring.")
        return

    if language == 'uz':
        await msg.answer(text="Tarjima uchun ma'lumotlar qabul qilindi.")
    elif language == 'ru':
        await msg.answer(text="Данные для перевода приняты.")
    else:
        await msg.answer(text="Translation information received.")

    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    for admin_id in admins:
        text = {
            'uz': f"Tarjima ma'lumotlari:\n{translation_info}",
            'ru': f"Данные для перевода:\n{translation_info}",
            'en': f"Translation details:\n{translation_info}"
        }.get(language, translation_info)

        try:
            await bot.send_message(chat_id=admin_id, text=f"""
{text}
Foydalanuvchi ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Ism: {tg_user['full_name']}
Username: @{msg.from_user.username}
Telefon-raqam: {tg_user['phone_number']}
""", parse_mode="HTML")
        except Exception:
            pass
    await state.finish()


# Matematik masalalarni so'rash
@dp.message_handler(Text(
    equals=["Matem va aniq fanlardan topshiriq yechib berish", "Решение заданий по математике и конкретным предметам",
            "Solving assignments in mathematics and concrete subjects"]))
async def math_request(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if language == 'uz':
        await msg.answer("""
Matematik masala uchun quyidagi ma'lumotlarni yuboring:
1. Masalaning matni yoki rasm.
""")
    elif language == 'ru':
        await msg.answer("""
Отправьте информацию для математической задачи:
1. Текст или изображение задачи.
""")
    else:  # English
        await msg.answer("""
Please send the information for the math problem:
1. The text or image of the problem.
""")
    await state.set_state("waiting_for_math_info")


@dp.message_handler(state="waiting_for_math_info", content_types=types.ContentTypes.ANY)
async def collect_math_info(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)

    if msg.content_type == "text":
        math_info = msg.text
    elif msg.content_type == "photo":
        math_info = "Rasm qabul qilindi."  # Rasm qabul qilindi
    else:
        await msg.answer("Iltimos, faqat matn yoki rasm yuboring.")
        return

    if language == 'uz':
        await msg.answer(text="Matematik masala uchun ma'lumotlar qabul qilindi.")
    elif language == 'ru':
        await msg.answer(text="Данные для математической задачи приняты.")
    else:
        await msg.answer(text="Math problem information received.")

    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    for admin_id in admins:
        text = {
            'uz': f"Matematik masala ma'lumotlari:\n{math_info}",
            'ru': f"Данные математической задачи:\n{math_info}",
            'en': f"Math problem details:\n{math_info}"
        }.get(language, math_info)

        try:
            await bot.send_message(chat_id=admin_id, text=f"""
{text}
Foydalanuvchi ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Ism: {tg_user['full_name']}
Username: @{msg.from_user.username}
Telefon-raqam: {tg_user['phone_number']}
""", parse_mode="HTML")
        except Exception:
            pass
    await state.finish()


@dp.message_handler(Text(equals=["Dasturlashga oid topshiriqni bajarib berish", "Выполняю задание по программированию",
                                 "Completing a programming assignment"]))
async def programming_task_request(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if language == 'uz':
        await msg.answer("Dasturlash topshiriqni yuboring:")
    elif language == 'en':
        await msg.answer("Please send the programming task:")
    else:  # Russian
        await msg.answer("Пожалуйста, отправьте задание по программированию:")

    await state.set_state("waiting_for_task_info")


@dp.message_handler(state="waiting_for_task_info")
async def collect_task_info(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)

    # Foydalanuvchidan topshiriq ma'lumotlarini olish
    task_info = msg.text

    if language == 'uz':
        await msg.answer("Dasturlash topshiriqi qabul qilindi.")
    elif language == 'en':
        await msg.answer("Programming task received.")
    else:
        await msg.answer("Задание по программированию получено.")

    # Administratorlarga topshiriqni yuborish
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f"""
Yangi dasturlash topshiriqi:
{task_info}
Foydalanuvchi ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
""", parse_mode="HTML")
        except Exception as e:
            print(f"Failed to send message to admin: {e}")

    await state.finish()


@dp.message_handler(Text(equals=[ui, ui_en, ui_ru, web, web_en, web_ru]))
async def order_selection(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)
    if msg.text == ui or msg.text == ui_en or msg.text == ui_ru:
        if language == 'uz':
            await msg.answer("Iltimos, UI uchun buyurtma ma'lumotlarini yuboring:")
        elif language == 'en':
            await msg.answer("Please send the order details for the UI:")
        else:
            await msg.answer("Пожалуйста, отправьте детали заказа для UI:")

        await state.set_state("waiting_for_ui_order_info")
    else:
        if language == 'uz':
            await msg.answer("Iltimos, web sayt uchun buyurtma ma'lumotlarini yuboring:")
        elif language == 'en':
            await msg.answer("Please send the order details for the web site:")
        else:
            await msg.answer("Пожалуйста, отправьте детали заказа для веб-сайта:")

        await state.set_state("waiting_for_web_order_info")


@dp.message_handler(state="waiting_for_ui_order_info")
async def collect_ui_order_info(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)

    # Foydalanuvchidan UI buyurtma ma'lumotlarini olish
    ui_order_info = msg.text.strip()

    if language == 'uz':
        await msg.answer("Buyurtma qabul qilindi.\n\n@prezintatsiyauz_admin\n@preuzadmin")
    elif language == 'en':
        await msg.answer("UI order received.\n\n@prezintatsiyauz_admin\n@preuzadmin")
    else:
        await msg.answer("Заказ UI принят.\n\n@prezintatsiyauz_admin\n@preuzadmin")

    # Administratorlarga UI buyurtmasini yuborish
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f"""
Yangi UI buyurtma:
{ui_order_info}
Foydalanuvchi ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
""", parse_mode="HTML")
        except Exception as e:
            print(f"Failed to send message to admin: {e}")

    await state.finish()


@dp.message_handler(state="waiting_for_web_order_info")
async def collect_web_order_info(msg: types.Message, state: FSMContext):
    language = await get_user_language(msg.from_user.id)

    # Foydalanuvchidan web sayt buyurtma ma'lumotlarini olish
    web_order_info = msg.text.strip()

    if language == 'uz':
        await msg.answer("Web sayt buyurtmasi qabul qilindi.")
    elif language == 'en':
        await msg.answer("Web order received.")
    else:
        await msg.answer("Заказ веб-сайта принят.")

    # Administratorlarga web sayt buyurtmasini yuborish
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f"""
Yangi web sayt buyurtma:
{web_order_info}
Foydalanuvchi ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
""", parse_mode="HTML")
        except Exception as e:
            print(f"Failed to send message to admin: {e}")

    await state.finish()


@dp.message_handler()
async def order_function(msg: types.Message, state: FSMContext):
    categories = json.loads(requests.get(url="http://127.0.0.1:8000/api/documents/").content)['results']
    txt = ''
    txt_en = ''
    txt_ru = ''
    for category in categories:
        if msg.text == category['name'] or msg.text == category['ru_name'] or msg.text == category['en_name']:
            if category['name'] == "Mustaqil ish" or category['name'] == "Ilmiy maqola" or category[
                'name'] == "Labaratoriya ishi va referat":
                async with state.proxy() as data:
                    data['name'] = msg.text
                    data['price'] = category['price']
                    data['test'] = 0
            else:
                async with state.proxy() as data:
                    data['name'] = msg.text
                    data['price'] = category['price']
                    data['test'] = 1
                    txt = "slayd"
                    txt_en = 'slide'
                    txt_ru = 'слайд'
            await state.set_state('page_number')
            language = await get_user_language(msg.from_user.id)
            if language == 'uz':
                await msg.answer(f"""
Siz {msg.text} ta’rif rejasinitanladingiz. Endi necha sahifa {txt} kerakligini raqamlar orqali kiriting. (Masalan 10, 15, 18 va h.k.)

{msg.text} 1 sahifa uchun {data['price']} uzs!""",
                                 reply_markup=await back_main_menu_button(msg.from_user.id))
            elif language == 'en':
                await msg.answer(f"""
You have selected the description plan {msg.text}. Now enter how many page {txt_en} you need by numbers. (For example 10, 15, 18, etc.)

{msg.text} {data['price']} uzs for 1 page!""",
                                 reply_markup=await back_main_menu_button(msg.from_user.id))
            else:
                await msg.answer(f"""
Вы выбрали план описания {msg.text}. Теперь введите числом необходимое количество {txt_ru} страниц. (Например, 10, 15, 18 и т. д.)

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
