import logging #Считывание логов
import asyncio #Для одновременной работы бота и парсинга
from aiogram import Bot, utils, types, Dispatcher, executor
from aiogram.types import ParseMode
from Config import TOKEN, URL
from database import ProcessSearchModel, initdatabase, FindIdSearch, FindAllCards
from parserq import ParseVideoCard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML) #Создание экземпляра бота и диспатчера
dp = Dispatcher(bot)

@dp.message_handler(commands="list") #Обработка команды
async def send_list(message: types.Message):
    cards = FindAllCards()
    for card in cards:
        card_title = card.title
        search_models = FindIdSearch(message.chat.id)
        for search_model in search_models:
            search_title = search_model.title
            if card_title.find(search_title) >= 0: #Если в загаловке есть подстрока поска, которую ищет пользователь, отправляем сообщение
                message_text = "строка поиска {} \r\n Найдено {}".format(search_title, utils.markdown.hlink(card_title, card.url))
                await message.answer(text=message_text, parse_mode=ParseMode.HTML) #Ответы пользователю

@dp.message_handler(commands="search")
async def send_list(message: types.Message):
    search_models = FindIdSearch(message.chat.id)
    for search_model in search_models:
        await message.answer(text=search_model.title)

@dp.message_handler()
async def echo(message: types.Message):
    await ProcessSearchModel(message)

async def scheduled(wait_for, parser):
    while True:
        await asyncio.sleep(wait_for)
        await parser.parse()

if __name__ == "__main__":
    initdatabase()
    parser = ParseVideoCard(url=URL, bot=bot)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10, parser))
    executor.start_polling(dp,skip_updates=True)