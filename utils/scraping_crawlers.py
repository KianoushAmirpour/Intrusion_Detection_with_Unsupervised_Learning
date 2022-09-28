# This file scrapes 3 websites to get the most up to date list of known crwalers

import os
from time import sleep
import datetime
import requests
from bs4 import BeautifulSoup as bs

now = datetime.datetime.now()
today = now.date()

# scraping the https://www.robotstxt.org/db.html
address_1 = "https://www.robotstxt.org/db.html"
url_1 = requests.get(address_1)
webpage_1 = bs(url_1.content, "lxml")
rows_1 = webpage_1.find("ol").find_all("li")
bots = [row.string for row in rows_1]

# #scraping the https://udger.com/resources/ua-list/crawlers
address_2 = "https://udger.com/resources/ua-list/crawlers"
url_2 = requests.get(address_2)
webpage_2 = bs(url_2.content, "lxml")
table = webpage_2.find("table")
table_rows = table.find_all("tr")
for tr in table_rows:
    if tr.find("b") == None:
        if tr.find("td") != None:
            data = tr.find("td").find("a")
            bots.append(data.text)
            
# scraping the https://user-agents.net/bots
address_3 = "https://user-agents.net/bots"
url_3 = requests.get(address_3)
webpage_3 = bs(url_3.content, "lxml")
bot_list = webpage_3.find("ul", attrs={"class": "compact_list"})
rows_2 = bot_list.find_all("li")
bots_from_webpage_3 = [row.string for row in rows_2]

bots.extend(bots_from_webpage_3)                     
with open(os.path.join("../input", f"known_crawlers_{today}.txt"), "w") as f:
    f.write("\n".join(set(bots)))
