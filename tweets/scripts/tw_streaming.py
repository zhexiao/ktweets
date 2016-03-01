from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
from pprint import pprint
from TwitterAPI import TwitterAPI
from datetime import datetime
import gevent, sys, os, redis, MySQLdb
import ujson as json
from config_import import *

# streaming class
class Streaming:
    def __init__(self):
        self.TW_CONSUMER_KEY = TW_CONSUMER_KEY
        self.TW_CONSUMER_SECRET = TW_CONSUMER_SECRET
        self.TW_TOKEN = TW_TOKEN
        self.TW_TOKEN_SECRET = TW_TOKEN_SECRET

        # set a limit pool thread for redis pub
        self.THREAD_POOL_SIZE = REDIS_POLL_SIZE
        self.pool = Pool(self.THREAD_POOL_SIZE)

        # connect db
        self.connect_db_redis()


    # define database connect
    def connect_db_mysql(self):
        db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset="utf8")
        return db


    # define redis connect
    def connect_db_redis(self):
        self.REDIS_CONF = {
            'host': REDIS_DB_HOST,
            'port': REDIS_PORT,
            'db': REDIS_DB_NUMBER,
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


    # redis publish method
    def redis_pub(self, tweet):
        try:
            for mention in tweet['entities']['user_mentions']:
                if mention['screen_name'] in self.users :
                   # pprint( 'redis publish %s, twitter id is %s, publish date %s'%("@{0}".format(mention['screen_name']), tweet['id_str'], datetime.now()) )
                   self.redis_conn.publish("@{0}".format(mention['screen_name']), json.dumps(tweet))
        except Exception as e:
            self.error_print(e)


    # get mysql mentions
    def get_db_mentions(self):
        try:
            db = self.connect_db_mysql()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            query = ('''SELECT * FROM twitter_mention order by id desc''')
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            db.close()

            mentions_data = []
            if rows:
                for mention in rows:
                    mentions_data.append(mention['name'])

            return mentions_data
        except Exception as e:
            self.error_print(e)


    # get the last mention id
    def get_last_mention_id(self):
        try:
            db = self.connect_db_mysql()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            query = ('''SELECT id FROM twitter_mention order by id desc limit 1''')
            cursor.execute(query)
            rows = cursor.fetchone()
            cursor.close()
            db.close()

            if rows:
                return rows['id']
            else:
                return None
        except Exception as e:
            self.error_print(e)



# initial class
stream = Streaming()
# get mention data
mentions_data = stream.get_db_mentions()
latest_mention_id = stream.get_last_mention_id()

# start running streaming
streaming_stopped = True
while True:
    try:
        # get the last insert mention id
        last_insert_mention_id = stream.get_last_mention_id()

        # check streaming is running or not
        if streaming_stopped:
            # running thread
            thread_m = gevent.spawn(stream.mention, mentions_data)

            # if thread start, set stop variable to false
            streaming_stopped = not thread_m.started

        # if last insert mention id is changed
        if last_insert_mention_id != latest_mention_id:
            # kill thread and get new mention data
            thread_m.kill()
            streaming_stopped = True
            mentions_data = stream.get_db_mentions()
            latest_mention_id = last_insert_mention_id


        gevent.sleep(10)
    except Exception as e:
        print(e)
