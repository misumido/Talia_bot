from database import get_db
from database.models import *
import pytz
from datetime import datetime
from all_text import answers
tashkent_timezone = pytz.timezone('Asia/Tashkent')
def get_all_users_tg_id():
    with next(get_db()) as db:
        users = db.query(Inactive_User).all()
        return [i.tg_id for i in users]

def get_users_count():
    with next(get_db()) as db:
        all_users = db.query(User).count()
        return all_users


def change_channel_db(url, id):
    with next(get_db()) as db:
        channel = db.query(AdminChannel).filter_by(id=1).first()
        channel.channel_url = url
        channel.channel_id = id
        db.commit()
def change_success_db(type, text=None, media_id=None):
    with next(get_db()) as db:
        message = db.query(AdminMessages).filter_by(id=1).first()
        message.type = type
        message.text = text
        message.media_id = media_id
        db.commit()
def change_info_message_db(type, text=None, media_id=None):
    with next(get_db()) as db:
        message = db.query(AdminMessages).filter_by(id=2).first()
        message.type = type
        message.text = text
        message.media_id = media_id
        db.commit()
def add_bonus_db(type, amount, text=None, media_id=None):
    with next(get_db()) as db:
        new = Materials(type=type, refs_amount=amount, text=text, media_id=media_id,
                        reg_date=datetime.now(tashkent_timezone))
        db.add(new)
        db.commit()
def add_utm_db(name):
    with next(get_db()) as db:
        new = AdminUTM(name=name, reg_date=datetime.now(tashkent_timezone))
        db.add(new)
        db.commit()
def check_link_db(name):
    with next(get_db()) as db:
        check = db.query(AdminUTM).filter_by(name=name).first()
        if check:
            return True
def get_utm_info_db():
    with next(get_db()) as db:
        info = db.query(AdminUTM).all()
        if info:
            return [[i.name, i.amount] for i in info]




#TODO для первого запуска чтобы создать базовые сообщения и тестовый канала
def create_channel_db():
    with next(get_db()) as db:
        check = db.query(AdminChannel).filter_by(id=1).first()
        if not check:
            channel = AdminChannel(reg_date=datetime.now())
            db.add(channel)
            db.commit()
def create_message_db():
    with next(get_db()) as db:
        new1 = AdminMessages(id=1, type="text", text=answers.get("success"))
        new2 = AdminMessages(id=2, type="text", text=answers.get("chan_info2"))
        db.add(new1)
        db.add(new2)
        db.commit()
