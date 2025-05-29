import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand, CallbackQuery, ReplyKeyboardRemove
from buttons import *
from states import *
from all_text import answers
from database.userservice import *
from utils import create_lid
bot_router = Router()

async def universal_messages_sender(info, message):
    channel = get_channel_db()
    if info[0] == "text":
        await message.bot.send_message(chat_id=message.from_user.id, text=info[1],
                                       reply_markup=await channels_univaersal_in(channel[1]))
    elif info[0] == "photo":
        if info[1]:
            await message.bot.send_photo(chat_id=message.from_user.id, photo=info[2],
                                         caption=info[1], reply_markup=await channels_univaersal_in(channel[1]))
        else:
            await message.bot.send_photo(chat_id=message.from_user.id, photo=info[2],
                                         reply_markup=await channels_univaersal_in(channel[1]))
    elif info[0] == "video":
        if info[1]:
            await message.bot.send_video(chat_id=message.from_user.id, video=info[2],
                                         caption=info[1], reply_markup=await channels_univaersal_in(channel[1]))
        else:
            await message.bot.send_video(chat_id=message.from_user.id, video=info[2],
                                         reply_markup=await channels_univaersal_in(channel[1]))
async def universal_bonus_sender(info, message, user_id):
    if info[0] == "text":
        await message.bot.send_message(chat_id=user_id, text=info[1])
    elif info[0] == "photo":
        if info[1]:
            await message.bot.send_photo(chat_id=user_id, photo=info[2],
                                         caption=info[1])
        else:
            await message.bot.send_photo(chat_id=user_id, photo=info[2])
    elif info[0] == "video":
        if info[1]:
            await message.bot.send_video(chat_id=user_id, video=info[2],
                                         caption=info[1])
        else:
            await message.bot.send_video(chat_id=user_id, video=info[2])

async def check_channels(message):
    channel = get_channel_db()
    try:
        check = await message.bot.get_chat_member(channel[0], user_id=message.from_user.id)
        if check.status in ["left"]:
            await message.bot.send_message(chat_id=message.from_user.id,
                                           text=answers.get("channel"),
                                           reply_markup=await channels_in(channel[1]))
            return False
    except:
        pass
    return True
@bot_router.callback_query(F.data.in_(["check_chan"]))
async def call_backs(query: CallbackQuery, state: FSMContext):
    if query.data == "check_chan":
        checking = await check_channels(query)
        await query.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        if checking:
            await query.bot.send_message(query.from_user.id, f"Menudan bo‘limni tanlang",
                                         reply_markup= await main_menu_bt())

@bot_router.message(CommandStart())
async def start(message: Message, state: FSMContext, command: BotCommand = None):
    checker = check_user(message.from_user.id)
    inviter = None
    if not checker:
        if command.args:
            link = decode_payload(command.args)
            inviter = get_inviter_by_link(link)
        await message.bot.send_message(chat_id=message.from_user.id, text=answers.get("name"))
        await state.set_state(Registration.name_st)
        if inviter:
            await state.set_data({"inviter": inviter})
        await asyncio.sleep(30)
        check_state1 = await state.get_state()
        if check_state1 == "Registration:name_st":
            await message.bot.send_message(chat_id=message.from_user.id, text=answers.get("name_wait1"))
            await asyncio.sleep(30)
            check_state2 = await state.get_state()
            if check_state2 == "Registration:name_st":
                await message.bot.send_message(chat_id=message.from_user.id, text=answers.get("name_wait2"))
                await state.clear()
    else:
        await message.bot.send_message(message.from_user.id, f"Menudan bo‘limni tanlang",
                                     reply_markup=await main_menu_bt())
@bot_router.message(Registration.name_st)
async def get_name(message: Message, state: FSMContext):
    if message.text:
        name = message.text
        await state.update_data({"name": name})
        await state.set_state(Registration.number_st)
        await message.bot.send_message(chat_id=message.from_user.id, text=answers.get("number"),
                                       reply_markup=await phone_bt())
        await asyncio.sleep(30)
        check_state1 = await state.get_state()
        if check_state1 == "Registration:number_st":
            await message.bot.send_message(chat_id=message.from_user.id, text=answers.get("number_wait1"))
            await asyncio.sleep(30)
            check_state2 = await state.get_state()
            if check_state2 == "Registration:number_st":
                await message.bot.send_message(chat_id=message.from_user.id, text=answers.get("number_wait2"),
                                               reply_markup=ReplyKeyboardRemove())
                await state.clear()
    else:
        await message.bot.send_message(chat_id=message.from_user.id, text=answers.get("again"))

@bot_router.message(Registration.number_st)
async def get_number(message: Message, state: FSMContext):
    if message.contact:
        data = await state.get_data()
        number = message.contact.phone_number
        name = data.get("name")
        inviter = data.get("inviter")
        if inviter:
            if isinstance(inviter, int):
                try:
                    add_refs_amount(inviter)
                    amount = get_refs_amount(inviter)
                    bonus = check_bonus_db(amount)
                    if bonus:
                        await message.bot.send_message(chat_id=inviter, text=f"Қўшган одамларингиз сони {amount} "
                                                                             f"тага етди! Совға дарсимни сизга тақдим этаман ❤️")
                        for i in bonus:
                            await universal_bonus_sender(i, message, inviter)
                    else:
                        await message.bot.send_message(chat_id=inviter,
                                                       text=f"Табриклайман! Сизнинг маҳсус ҳаволангиз орқали каналга "
                                                            f"{amount} та иштирокчи қўшилди")
                except:
                    pass
            else:
                add_utm_amount(inviter)
        add_user(tg_id=message.from_user.id, name=name, phone=number, inviter=inviter)
        create_lid(name, number)
        await state.clear()
        success = get_success_message_db()
        await universal_messages_sender(success, message)
        for_mm = await message.bot.send_message(chat_id=message.from_user.id, text="Рўйхатдан ўтдингиз",
                                       reply_markup=await main_menu_bt())
        check_chan = await check_channels(message)
        await asyncio.sleep(250)
        chan_info = get_message2_db()
        await universal_messages_sender(chan_info, message)
    else:
        await message.bot.send_message(chat_id=message.from_user.id, text=answers.get("again"))

@bot_router.message(F.text=="🔢Mening havolam orqali o‘tganlar soni")
async def ref_count(message: Message):
    channels_checker = await check_channels(message)
    if channels_checker:
        amount = get_refs_amount(message.from_user.id)
        await message.bot.send_message(chat_id=message.from_user.id,
                                       text=f"{answers.get("ref_count1")}"  
                                            f"{amount}{answers.get("ref_count2")}")
@bot_router.message(F.text=="🔗Mening taklif havolam")
async def ref_link(message: Message):
    channels_checker = await check_channels(message)
    if channels_checker:
        link = await create_start_link(message.bot, str(message.from_user.id), encode=True)
        await message.bot.send_message(chat_id=message.from_user.id,
                                       text=f"Sizning taklif havolangiz:\n{link}")
@bot_router.message(F.text=="⭐️Menga mavjud bo‘lgan bonuslar")
async def user_bonus(message: Message):
    channels_checker = await check_channels(message)
    if channels_checker:
        info = all_bonuses_db(message.from_user.id)
        print(info)
        if info:
            for i in info:
                await universal_bonus_sender(i, message, message.from_user.id)
