from Config import DRIVERPATH, URL
from requests import *
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from database import FindAllSearch, process_video_card

class ParseVideoCard:
    def __init__(self, url, bot):
        self.driver = webdriver.Chrome(executable_path=DRIVERPATH)
        self.driver.minimize_window()
        self.url = url
        self.bot = bot
    def __del__(self):
        self.driver.close()

    async def parse(self):
        search_models = FindAllSearch()
        for page in range(1, 16):
            print(self.url.format(page))
            self.driver.get(self.url.format(page))
            items = len(self.driver.find_elements_by_class_name("catalog-products view-simple"))
            for items in range(items):
                cards = self.driver.find_elements_by_class_name("catalog-products view-simple")
                for card in cards:
                    product_item = card.find_element_by_class_name("catalog-product__name ui-link ui-link_black") #Получаем конкретный элемент
                    card_title = product_item.text
                    card_href = product_item.get_attribute("href")
                    for search_model in search_models: #Ищет ли видеокарту какой либо из пользователей
                        if card_title.find(search_model.title) >=0:
                            await process_video_card(card_title, card_href, search_model.chatid, self.bot)
                