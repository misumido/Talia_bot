from database import get_db
from database.models import *
from datetime import datetime
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import Session
import pytz
tashkent_timezone = pytz.timezone('Asia/Tashkent')

def check_user(tg_id):
    with next(get_db()) as db:
        checker = db.query(User).filter_by(tg_id=int(tg_id)).first()
        check2 = db.query(Inactive_User).filter_by(tg_id=int(tg_id)).first()
        if not check2:
            new_user = Inactive_User(tg_id=tg_id, reg_date=datetime.now(tashkent_timezone))
            db.add(new_user)
            db.commit()
        if checker:
            return True
        return False
def add_user(tg_id, name, phone,inviter):
    with next(get_db()) as db:
        new_user = User(tg_id=int(tg_id), name=name, phone_number=phone,
                        inviter=inviter,reg_date=datetime.now(tashkent_timezone))
        db.add(new_user)
        db.commit()

def get_inviter_by_link(link):
    with next(get_db()) as db:
        check_tg = db.query(User).filter_by(tg_id=int(link)).first()
        check_utm = db.query(AdminUTM).filter_by(name=link).first()
        if check_tg:
            return check_tg.tg_id
        elif check_utm:
            return check_utm.name
        return False

def get_refs_amount(tg_id):
    with next(get_db()) as db:
        check_tg = db.query(User).filter_by(tg_id=int(tg_id)).first()
        if check_tg:
            return check_tg.ref_amount
        return 0
def add_refs_amount(tg_id):
    with next(get_db()) as db:
        check_tg = db.query(User).filter_by(tg_id=int(tg_id)).first()
        if check_tg:
            check_tg.ref_amount += 1
            db.commit()

def add_utm_amount(name):
    with next(get_db()) as db:
        check_utm = db.query(AdminUTM).filter_by(name=name).first()
        if check_utm:
            check_utm.amount += 1
            db.commit()


def check_link(link):
    with next(get_db()) as db:
        user = db.query(User).filter_by(user_link=link).first()
        if user:
            return True
        return False

def get_channel_db():
    with next(get_db()) as db:
        channel = db.query(AdminChannel).filter_by(id=1).first()
        return [channel.channel_id, channel.channel_url]

def get_success_message_db():
    with next(get_db()) as db:
        info = db.query(AdminMessages).filter_by(id=1).first()
        return [info.type, info.text, info.media_id]
def get_message2_db():
    with next(get_db()) as db:
        info = db.query(AdminMessages).filter_by(id=2).first()
        return [info.type, info.text, info.media_id]

def check_bonus_db(amount):
    with next(get_db()) as db:
        check = db.query(Materials).filter_by(refs_amount=amount).all()
        if check:
            return [[i.type, i.text, i.media_id] for i in check]
def free_bonuses_db():
    with next(get_db()) as db:
        check = db.query(Materials).filter_by(refs_amount=0).all()
        if check:
            return [[i.type, i.text, i.media_id] for i in check]

def all_bonuses_db(tg_id):
    with next(get_db()) as db:
        refs = get_refs_amount(tg_id)
        bonuses = db.query(Materials).filter(Materials.refs_amount <= refs).all()
        if bonuses:
            return [[i.type, i.text, i.media_id] for i in bonuses]
def test_db(tg_id):
    with next(get_db()) as db:
        check_tg = db.query(User).filter_by(tg_id=int(tg_id)).first()
        if check_tg:
            check_tg.ref_amount += 1000
            db.commit()