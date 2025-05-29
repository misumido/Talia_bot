from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
async def phone_bt():
    buttons = [[KeyboardButton(text="📲Raqam yuborish", request_contact=True)]]
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return kb
async def channels_in(channel):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Каналимиз", url=channel)
    keyboard_builder.button(text="Obuna bo‘lganligizni tekshirish", callback_data="check_chan")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
async def channels_univaersal_in(channel):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Каналимиз", url=channel)
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

async def main_menu_bt():
    buttons = [
        [KeyboardButton(text="🔗Mening taklif havolam")],
        [KeyboardButton(text="🔢Mening havolam orqali o‘tganlar soni")],
        [KeyboardButton(text="⭐️Menga mavjud bo‘lgan bonuslar")],
        ]
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return kb

async def cancel_in():
    buttons = [
        [InlineKeyboardButton(text="❌Отменить отправку", callback_data="cancel")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb
async def change_messages_in():
    buttons = [
        [InlineKeyboardButton(text="Сообщение с ссылкой на канал", callback_data="change_message_success")],
        [InlineKeyboardButton(text="Сообщение после ссылки", callback_data="change_chan_info")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb




async def admin_menu_in():
    buttons = [
        [InlineKeyboardButton(text="✉️Рассылка", callback_data="mailing")],
        [InlineKeyboardButton(text="Добавить UTM", callback_data="add_utm")],
        [InlineKeyboardButton(text="Статистика UTM", callback_data="utm_info")],
        [InlineKeyboardButton(text="Таблица юзеров", callback_data="excel_users")],
        [InlineKeyboardButton(text="Таблица UTM", callback_data="excel_utm")],
        [InlineKeyboardButton(text="Добавить бонус", callback_data="add_bonus")],
        [InlineKeyboardButton(text="Изменить сообщение", callback_data="change_message")],
        [InlineKeyboardButton(text="Изменить ссылку на канал", callback_data="change_channel")],
        [InlineKeyboardButton(text="Закрыть", callback_data="cancel")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def cancel_bt():
    buttons = [
        [KeyboardButton(text="❌Отменить")]
    ]
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return kb