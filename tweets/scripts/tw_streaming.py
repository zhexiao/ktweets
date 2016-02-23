from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
from pprint import pprint
from TwitterAPI import TwitterAPI
from datetime import datetime
import gevent, sys, os, redis, MySQLdb
import ujson as json


# define database connect
def connectDb():
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="kweets", charset="utf8")
    return db


# streaming class
class Streaming:
    def __init__(self):
        self.TW_CONSUMER_KEY = 'uEgl4FaX6FEP0H578gocLsTMe'
        self.TW_CONSUMER_SECRET = 'C4tPkIhjRKg4pj5qCEKAAclpAUt3s0KdDmobSzJkovcQEsEYMA'
        self.TW_TOKEN = '2820265982-jYjVyzNb7vm96Lk3f1uzvRJt91OyC39ni8TD5q7'
        self.TW_TOKEN_SECRET = '5ID7bK6Zp8j81W9I1sXxTwiltYKQwsKZE4o8pzLLK4ico'

        # set a limit pool thread for redis pub
        self.THREAD_POOL_SIZE = 200
        self.pool = Pool(self.THREAD_POOL_SIZE)

        # init redis connection
        self.REDIS_CONF = {
            'host': 'localhost',
            'port': 6379,
            'db': 1,
        }
        self.redis_conn = redis.StrictRedis( **self.REDIS_CONF )


    # show error function
    def error_print(self, message):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, message, fname, exc_tb.tb_lineno)


    # twitter mention api
    def mention(self, users):
        self.users = users

        while True:
            try:
                api = TwitterAPI(self.TW_CONSUMER_KEY, self.TW_CONSUMER_SECRET, self.TW_TOKEN, self.TW_TOKEN_SECRET)
                tracks_data = { 'track' : "@{0}".format( ",@".join(self.users ) ) }

                stream_res = api.request('statuses/filter', tracks_data).get_iterator()
                for item in stream_res:
                    # omit retweets
                    if 'retweeted_status' in item:
                        continue

                    if 'text' in item:
                        self.pool.spawn(self.redis_pub, item)
            except Exception as e:
                self.error_print(e)


    def redis_pub(self, tweet):
        try:
            for mention in tweet['entities']['user_mentions']:
                if mention['screen_name'] in self.users :
                   # pprint( 'redis publish %s, twitter id is %s, publish date %s'%("@{0}".format(mention['screen_name']), tweet['id_str'], datetime.now()) )
                   self.redis_conn.publish("@{0}".format(mention['screen_name']), json.dumps(tweet))
        except Exception as e:
            self.error_print(e)




# get mentions
def getMentions():
    db = connectDb()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    query = ('''SELECT name FROM twitter_mention''')
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


# mention container
mentions_data = []
mentions_res = getMentions()
for men in mentions_res:
    mentions_data.append(men['name'])


# initial class
stream = Streaming()
gevent.joinall([
    gevent.spawn(stream.mention, mentions_data)
])
