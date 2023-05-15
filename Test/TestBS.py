import requests
from bs4 import BeautifulSoup as BS

r = requests.get("https://store.softline.ru/parts/videocards/?page=1")
print(r)
html = BS(r.content, "html.parser")
for el in html.select("h5"):
    print(el)
