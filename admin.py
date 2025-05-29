from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from buttons import *
from states import ChangeAdminInfo
from aiogram.utils.deep_linking import create_start_link
from database.adminservice import *
from aiogram.types.input_file import FSInputFile
from excel_converter import convert_to_excel
import re
import os
# TODO id admina
admins_id = [305896408, ]
admin_router = Router()
# create_message_db()
# create_channel_db()
@admin_router.message(Command(commands=["admin"]))
async def admin_mm(message: Message):
    if message.from_user.id in admins_id:
        count = get_users_count()
        await message.bot.send_message(message.from_user.id, f"🕵Панель админа\n"
                                                             f"Количество зарегистрированных юзеров в боте: {count}",
                                       reply_markup=await admin_menu_in())
@admin_router.callback_query(F.data.in_(["cancel", "none",
                                         "mailing", "excel_users", "excel_utm", "change_channel",
                                         "change_message", "change_message_success","change_chan_info",
                                         "add_bonus", "add_utm", "utm_info"]))
async def call_backs(query: CallbackQuery, state: FSMContext):
    await state.clear()
    if query.data == "cancel":
        await query.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        await state.clear()
    elif query.data == "none":
        pass
    elif query.data == "mailing":
        await query.bot.send_message(query.from_user.id, "Введите сообщение для рассылки, либо отправьте фотографии/видео с описанием",
                                     reply_markup=await cancel_bt())
        await state.set_state(ChangeAdminInfo.mailing)
    elif query.data == "excel_users":
        try:
            file = convert_to_excel("user")
            document = FSInputFile(file)
            await query.bot.send_document(query.from_user.id, document)
            os.remove(file)
        except:
            await query.bot.send_message(query.from_user.id, "Произошла ошибка")
    elif query.data == "excel_utm":
        try:
            file = convert_to_excel("utm")
            document = FSInputFile(file)
            await query.bot.send_document(query.from_user.id, document)
            os.remove(file)
        except:
            await query.bot.send_message(query.from_user.id, "Произошла ошибка")
    elif query.data == "change_channel":
        await query.bot.send_message(query.from_user.id, "Введите ссылку на канал (формат: t.me/ или https://t.me/)",
                                     reply_markup=await cancel_bt())
        await state.set_state(ChangeAdminInfo.get_channel_url)
    elif query.data == "change_message":
        await query.bot.send_message(query.from_user.id, "Какое сообщение сменить?",
                                     reply_markup=await change_messages_in())

    elif query.data == "change_message_success":
        await query.bot.send_message(query.from_user.id, "Отправьте текст/фото с описанием/видео с описанием",
                                     reply_markup=await cancel_bt())
        await state.set_data({"what": "success"})
        await state.set_state(ChangeAdminInfo.change_message)
    elif query.data == "change_chan_info":
        await query.bot.send_message(query.from_user.id, "Отправьте текст/фото с описанием/видео с описанием",
                                     reply_markup=await cancel_bt())
        await state.set_data({"what": "info"})
        await state.set_state(ChangeAdminInfo.change_message)
    elif query.data == "add_bonus":
        await query.bot.send_message(query.from_user.id, "Введите количество рефералов за бонус",
                                     reply_markup=await cancel_bt())
        await state.set_state(ChangeAdminInfo.bonus_amount)
    elif query.data == "add_utm":
        await query.bot.send_message(query.from_user.id, f"Введите название UTM. Оно должно содержать только "
                                                         f"английские буквы, цифры и нижнее подчеркивание.Допустимый размер - от 7 до 30 символов.",
                                     reply_markup=await cancel_bt())
        await state.set_state(ChangeAdminInfo.bonus_amount)
    elif query.data == "utm_info":
        info = get_utm_info_db()
        text = "Информация UTM:\n\n"
        count = 1
        if info:
            for i in info:
                link = await create_start_link(query.bot, str(i[0]), encode=True)
                text += f"{count}. {i[0]}: {i[1]} переходов.\n Ссылка: {link}\n\n"
                count += 1
            await query.bot.send_message(query.from_user.id, text)
        else:
            await query.bot.send_message(query.from_user.id, "Нет активных UTM")




@admin_router.message(ChangeAdminInfo.utm)
async def add_utm(message: Message, state: FSMContext):
    if message.text:
        check = check_link_db(message.text)
        pattern = r'^[a-zA-Z0-9_]+$'
        check_pattern = re.search(pattern, message.text)
        if not check:
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text="📛 Такая название уже используется ;(\n"
                                                "Попробуйте заново",
                                           reply_markup= await main_menu_bt())
            await state.clear()
        elif check_pattern and 6 < len(message.text) < 31:
            link = await create_start_link(message.bot, str(message.from_user.id), encode=True)
            add_utm_db(message.text)
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text=f"Новая UTM {message.text}:\n\n"
                                                f"{link}")
            await state.clear()
        else:
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text="Ошибка! 📛 Новая ссылка должна содержать только английские буквы, цифры и нижнее подчеркивание.\n"
                                                "Допустимый размер - от 7 до 30 символов.\n\n"
                                                "Попробуйте заново",
                                           reply_markup=await main_menu_bt())
            await state.clear()
    else:
        await message.bot.send_message(message.from_user.id, "️️❗Ошибка! Введите корректное значение", reply_markup=await main_menu_bt())
        await state.clear()

@admin_router.message(ChangeAdminInfo.bonus_amount)
async def get_bonus_amount(message: Message, state: FSMContext):
    if message.text == "❌Отменить":
        await message.bot.send_message(message.from_user.id, "🚫Действие отменено", reply_markup=await main_menu_bt())
        await state.clear()
    elif message.text.isdigit():
        await state.set_data({"amount": int(message.text)})
        await message.bot.send_message(message.from_user.id, text="Отправьте текст/фото с описанием/видео с описанием бонуса",
                                       reply_markup=await cancel_bt())
        await state.set_state(ChangeAdminInfo.bonus_info)
    else:
        await message.bot.send_message(message.from_user.id, "️️❗Ошибка! Введите корректное число", reply_markup=await main_menu_bt())
        await state.clear()
@admin_router.message(ChangeAdminInfo.bonus_info)
async def get_bonus_info(message: Message, state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount")
    if message.text == "❌Отменить":
        await message.bot.send_message(message.from_user.id, "🚫Действие отменено", reply_markup=await main_menu_bt())
        await state.clear()
    else:
        await state.clear()
        if message.text:
            add_bonus_db(type="text", amount=amount, text=message.text)
            await message.bot.send_message(message.from_user.id, "️Бонус добавлен")
        elif message.photo:
            if message.caption:
                add_bonus_db(type="photo",amount=amount, text=message.caption, media_id=message.photo[-1].file_id)
                await message.bot.send_message(message.from_user.id, "️Бонус добавлен")
            else:
                add_bonus_db(type="photo",amount=amount, media_id=message.photo[-1].file_id)
                await message.bot.send_message(message.from_user.id, "️Бонус добавлен")
        elif message.video:
            if message.caption:
                add_bonus_db(type="video",amount=amount, text=message.caption, media_id=message.video.file_id)
                await message.bot.send_message(message.from_user.id, "️Бонус добавлен")
            else:
                add_bonus_db(type="video",amount=amount, media_id=message.video.file_id)
                await message.bot.send_message(message.from_user.id, "️Бонус добавлен")

        else:
            await message.bot.send_message(message.from_user.id, "️️❗Ошибка", reply_markup=await main_menu_bt())
            await state.clear()


@admin_router.message(ChangeAdminInfo.change_message)
async def change_message(message: Message, state: FSMContext):
    data = await state.get_data()
    what = data.get("what")
    if message.text == "❌Отменить":
        await message.bot.send_message(message.from_user.id, "🚫Действие отменено", reply_markup=await main_menu_bt())
        await state.clear()
    else:
        await message.bot.send_message(message.from_user.id, "️Сообщение изменено")
        await state.clear()
        if message.text:

            if what == "success":
                change_success_db(type="text", text=message.text)
            elif what == "info":
                change_info_message_db(type="text", text=message.text)
        elif message.photo:
            if message.caption:
                if what == "success":
                    change_success_db(type="photo", text=message.caption, media_id=message.photo[-1].file_id)
                elif what == "info":
                    change_info_message_db(type="photo", text=message.caption, media_id=message.photo[-1].file_id)
            else:
                if what == "success":
                    change_success_db(type="photo", media_id=message.photo[-1].file_id)
                elif what == "info":
                    change_info_message_db(type="photo", media_id=message.photo[-1].file_id)
        elif message.video:
            if message.caption:
                if what == "success":
                    change_success_db(type="video", text=message.caption, media_id=message.video.file_id)
                elif what == "info":
                    change_info_message_db(type="video", text=message.caption, media_id=message.video.file_id)
            else:
                if what == "success":
                    change_success_db(type="video", media_id=message.video.file_id)
                elif what == "info":
                    change_info_message_db(type="video", media_id=message.video.file_id)
        else:
            await message.bot.send_message(message.from_user.id, "️️❗Ошибка", reply_markup=await main_menu_bt())
            await state.clear()


@admin_router.message(ChangeAdminInfo.mailing)
async def mailing_admin(message: Message, state: FSMContext):
    if message.text == "❌Отменить":
        await message.bot.send_message(message.from_user.id, "🚫Действие отменено", reply_markup=await main_menu_bt())
        await state.clear()
    else:
        all_users = get_all_users_tg_id()
        success = 0
        unsuccess = 0
        for i in all_users:
            try:
                await message.bot.copy_message(chat_id=i, from_chat_id=message.from_user.id,
                                               message_id=message.message_id, reply_markup=message.reply_markup)
                success += 1
            except:
                unsuccess +=1
        await message.bot.send_message(message.from_user.id, f"Рассылка завершена!\n"
                                                             f"Успешно отправлено: {success}\n"
                                                             f"Неуспешно: {unsuccess}", reply_markup=await main_menu_bt())
        await state.clear()
@admin_router.message(ChangeAdminInfo.get_channel_url)
async def get_new_channel_url(message: Message, state: FSMContext):
    if message.text == "❌Отменить":
        await message.bot.send_message(message.from_user.id, "🚫Действие отменено", reply_markup=await main_menu_bt())
        await state.clear()
    elif "t.me/" in message.text.lower() or "https://t.me/" in message.text.lower():
        await state.set_data({"chan_url": message.text})
        await message.bot.send_message(message.from_user.id, "Введите ID канала\n"
                                                             "Узнать ID можно переслав любой "
                                                             "пост из вашего канала в бот @getmyid_bot. "
                                                             "После скопируйте результат из графы 'Forwarded from chat:'",
                                       reply_markup=await cancel_bt())
        await state.set_state(ChangeAdminInfo.get_channel_id)
    else:
        await message.bot.send_message(message.from_user.id, "️️❗Ошибка! Введите корректную ссылку", reply_markup=await main_menu_bt())
        await state.clear()
@admin_router.message(ChangeAdminInfo.get_channel_id)
async def get_new_channel_id(message: Message, state: FSMContext):
    if message.text == "❌Отменить":
        await message.bot.send_message(message.from_user.id, "🚫Действие отменено", reply_markup=await main_menu_bt())
        await state.clear()
    elif message.text:
        try:
            chanel_url = await state.get_data()
            channel_id = int(message.text)
            if channel_id > 0:
                channel_id *= -1
            new_channel = change_channel_db(url=chanel_url["chan_url"], id=channel_id)
            if new_channel:
                await message.bot.send_message(message.from_user.id, f"Канал изменен ✅\n"
                                                                     f"❗️Не забудьте добавить бота в этот канал и дать ему админку❗️",
                                               reply_markup=await main_menu_bt())
                await state.clear()
            else:
                await message.bot.send_message(message.from_user.id, f"Подписка не добавлена.",
                                               reply_markup=await main_menu_bt())
                await state.clear()
        except:
            await message.bot.send_message(message.from_user.id, "🚫Не удалось добавить подписку. Данная подписка уже существует",
                                           reply_markup=await main_menu_bt())
            await state.clear()
    else:
        await message.bot.send_message(message.from_user.id, "️️❗Ошибка", reply_markup=await main_menu_bt())
        await state.clear()

@admin_router.message(F.text=="❌Отменить")
async def profile(message: Message, state: FSMContext):
    await message.bot.send_message(message.from_user.id, "️️Все действия отменены", reply_markup=await main_menu_bt())
    await state.clear()
