from aiogram.types import ParseMode
from aiogram import utils
from peewee import * #Для работы с бд

db = SqliteDatabase("VC.db")

class BaseModel(Model):  #База
    class Meta:
        database = db

class VideoCard(BaseModel):  #Основная табличка
    title = CharField()
    url = TextField()

class SearchModel(BaseModel):  #Ключевые слова
    title = CharField()  #Что ищет пользователь
    chatid = CharField()  #ID пользователя

def FindAllCards():
    return VideoCard.select()
def FindIdSearch(chat_id):
    return SearchModel.select().where(SearchModel.chatid == chat_id) #Что бы отвечать конкретному пользователю
def FindAllSearch():
    return SearchModel.select()

async def ProcessSearchModel(message):  #Функция добавления ключевых слов
    search_exist = True
    try:
        search = SearchModel.select().where(SearchModel.title == message.text).get() #Пытаемся найти ключевое слово в бд
        search.delete_instance()
        await message.answer("{} Говоришь? Ок, забыли.".format(message.text))
        return search_exist
    except DoesNotExist as de:
        search_exist = False
    if not search_exist:
        rec = SearchModel(title=message.text, chatid = message.chat.id)
        rec.save()
        await message.answer("Понял, {} добавленна в критерии.".format(message.text))
    else:
        await message.answer("строка поиска {} уже есть".format(message.text))
    return search_exist


async def process_video_card(title, url, chat_id, bot):
    card_exist = True
    try:
        card = VideoCard.select().where(VideoCard.title == title).get()
    except DoesNotExist as de:
        card_exist = False
    if not card_exist:
        rec = VideoCard(title=title, url=url)  #Добавляем карту, которой до этого не было в бд
        rec.save()
        message_text = utils.markdown.hlink(title, url)
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=ParseMode.HTML)
    return card_exist

def initdatabase():  #Инициализация базы данных
    db.create_tables([VideoCard, SearchModel])