# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
 # -*- coding: utf-8 -*-
from contextlib import closing
from datetime import datetime
import MySQLdb as mdb


class InsomniaPipeline(object):
    def __init__(self):
        with open('DB.txt') as settings:
            self.CONFIG = {x.split('=')[0].strip(): x.split('=')[1].strip() for x in settings.readlines()}
        if not self.CONFIG:
            exit()

    def open_mysql(self):
        self.conn = mdb.connect(user=self.CONFIG['USERNAME'], passwd=self.CONFIG['PASSWORD'], db=self.CONFIG['DATABASE'], host=self.CONFIG['HOST'], charset="utf8", use_unicode=True)
        self.conn.autocommit(True)

    def close_mysql(self):
        self.conn.close()
    
    def doQuery(self, cursor, query, item):
        try:
            cursor.execute(query, [item['post_id'], item['date'].strftime('%Y-%m-%d %H:%M:%S'), item['url'], item['title'], item['text'], item['username'], item['question']])
        except mdb.Error, e:
            print "Error = %d, %s" % (e.args[0], e.args[1])

        return self.conn.insert_id() or 0

        
    def process_item(self, item, spider):
    	self.open_mysql()
    	with closing(self.conn.cursor()) as cursor:
    		self.doQuery(cursor, "INSERT INTO insomnia (postid, thedate, url, title, text, username, question) VALUES (%s, %s, %s, %s, %s, %s, %s)", item)
        self.close_mysql()
        return item

