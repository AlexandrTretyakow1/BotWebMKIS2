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

@dp.message_handler(commands="start") #Приветственная команда
async def firstAnswer(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Ты кто?")],
        [types.KeyboardButton(text="Я кто?")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Дарова. По какому вопросу?", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Ты кто?" or message.text == "Я кто?")  #Вступительный диалог
async def secondAnswer(message: types.Message):
    kb = [
        [types.KeyboardButton(text="...")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Тут такие вопросы задавать не принято. Мы оба понимаем зачем ты здесь.",reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "..." or message.text == "Нужна помощь...") #Пояснение работы бота.
async def InfoAnswer(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Мои критерии")],
        [types.KeyboardButton(text="Начать поиск")],
        [types.KeyboardButton(text="Нужна помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(
        "Я ищу тебе видеокарты по доступным ценам, а ты... Впрочем, мне не важно что ты будешь делать с этой информацией."
        "\r\n\r\nДля того, чтобы начать поиск, просто назови мне критерии. Если хочешь найти видюхи сороковой серии, напиши 40, если что то от MSI - пиши MSI. "
        "Понятно? Можешь говорить и несколько критериев сразу, но учти, отправлять их нужно по отдельности. "
        "Так же, на несколько критериев одновременно (ASUS, 1080) я покажу тебе все видеокарты, которые соответствуют хотя бы одному критерию."
        "\r\nДля того, чтобы убрать критерий, просто напиши его повторно."
        "\r\n\r\nКак закончишь с критериями, я смогу начать поиск: \r\nНачать поиск"
        "\r\nИ еще, разрешаю уточнять что ты вообще ищешь: \r\nМои критерии"
        "\r\nЕсли запутался, я могу еще раз повторить как все работает: \r\nНужна помощь",
        reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Начать поиск") #Обработка команды пользователя. Вывод найденных карт
async def send_list(message: types.Message):
    cards = FindAllCards()
    for card in cards:
        card_title = card.title
        search_models = FindIdSearch(message.chat.id)
        for search_model in search_models:
            search_title = search_model.title
            if card_title.find(search_title) >= 0: #Если в загаловке есть подстрока поска, которую ищет пользователь, отправляем сообщение
                message_text = "Ну, смотри. По поводу {},\r\nесть вот такой аппарат {}".format(search_title, utils.markdown.hlink(card_title, card.url))
                await message.answer(text=message_text, parse_mode=ParseMode.HTML) #Ответы пользователю

@dp.message_handler(lambda message: message.text == "Мои критерии")
async def send_list(message: types.Message):
    search_models = FindIdSearch(message.chat.id)
    await message.answer(text="Смотри, мы собираемся искать:")
    for search_model in search_models:
        await message.answer(text=search_model.title)
    await message.answer(text="Если хочешь что то убрать из этого списка, просто напиши критерий повторно (в любой момент)")


@dp.message_handler()
async def psm(message: types.Message):
    await ProcessSearchModel(message)

async def scheduled(wait_for, parser):
    while True:
        await asyncio.sleep(wait_for)
        print("parse") #await parser.parse() для работы парсера. Пасс потом можно убрать.
        pass

if __name__ == "__main__":
    initdatabase() #Для инициализации парсера, добавить parser = ParseVideoCard(url=URL, bot=bot)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10, None)) #None заменить на parser
    executor.start_polling(dp,skip_updates=True)