from collections import Counter
import dateutil.parser
import feedparser
from itertools import tee, islice
import json
import re
import sqlite3

def ngrams(lst, n):
  tlst = lst
  while True:
    a, b = tee(tlst)
    l = tuple(islice(a, n))
    if len(l) == n:
      yield l
      next(b)
      tlst = b
    else:
      break
	  
def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    return re.sub(r'<[^>]*?>', '', value.encode('utf-8', 'ignore'))

def get_data():
	#TODO:
	#	- Get new articles since last update
	#   - store website name in database
	feed_url = 'http://econsultancy.com/uk/blog.atom'
	feed = feedparser.parse(feed_url)
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	last_id = 3

	to_insert=[]
	for entry in feed.entries:
		yourdate = dateutil.parser.parse(entry.updated.encode('ascii', 'ignore'))
		entry_date = str(yourdate.year)+"-"+str(yourdate.month)+"-"+str(yourdate.day)
		post_content = strip_tags(entry.content[0].value.encode('ascii', 'ignore'))
		insert_statement = "INSERT INTO data (title, date, body) VALUES ( %s, %s, %s)" % ("title", entry_date, post_content) 
		print "Going to insert:",insert_statement 
		c.execute("INSERT INTO data (title, date, body) VALUES ( ?, ?, ?)", (entry['title'], entry_date, post_content))
		
		#to_insert.append(( entry.title.encode('ascii', 'ignore'), entry_date, entry.content[0].value.encode('ascii', 'ignore')))	
		
	print to_insert
	#cur.executemany("INSERT INTO buzzmon.data (title, date, body) VALUES ( %s, %s, %s)", to_insert) 
		
	conn.commit()
	conn.close()

def get_word_count():
	""" Get word count"""
	
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	c.execute("SELECT body FROM DATA")
	all_text = ""
	for row in c:
		all_text += row[0].encode('ascii', 'ignore')

	print "here"
	all_text = all_text.translate(None, '!?;":(),-.')
	
	all_text = all_text.lower()
	
	all_words = []
	all_words = all_text.split()
	
	wc = Counter(all_words)
	for x in wc.keys()[0:10]:
		print x, " - ", wc[x]
		
	return wc
	
print "here"	
get_word_count()	
	
"""12:35
Count the number of words 

"""