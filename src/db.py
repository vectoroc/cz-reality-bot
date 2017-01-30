from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime
import json

db = SqliteExtDatabase('reality.db')

class BaseModel(Model):
    class Meta:
        database = db

class Flat(BaseModel):
    id = IntegerField(sequence=0, primary_key=True)
    hash = CharField(index=True)
    url = TextField()
    title = CharField()
    text = TextField()
    price = CharField(max_length=64)
    data = TextField(help_text='json meta')
    created_date = DateTimeField(default=datetime.datetime.now)
    is_sent = BooleanField(default=False)

    @staticmethod
    def update_or_create(data):
        try:
            Flat.get(Flat.hash == data['hash'])
        except Flat.DoesNotExist:
            Flat.create(price=data['price'], hash=data['hash'], title=data['title'], text=data['text'], data=json.dumps(data), url=data['url'])



class FlatImages(BaseModel):
    id = IntegerField(primary_key=True)
    flatId = ForeignKeyField(Flat, related_name='images')
    url = TextField()


class Chat(BaseModel):
    id = IntegerField(primary_key=True)
    data = TextField()

    @staticmethod
    def register(chat):
        try:
            Chat.get(Chat.id == chat.id)
        except Chat.DoesNotExist:
            Chat.create(id=chat.id, data=json.dumps(chat.__dict__))


tables = [Flat, FlatImages, Chat]

def db_create_tables():
    db.create_tables(tables)

def db_drop_tables():
    db.drop_tables(tables)