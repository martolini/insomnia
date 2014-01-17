# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class InsomniaItem(Item):
    post_id = Field()
    date = Field()
    url = Field()
    title = Field()
    text = Field()
    username = Field()
    question = Field()