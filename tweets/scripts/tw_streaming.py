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


    # twitter track api
    def twitter_track(self, track_text):
        self.track_text = track_text

        try:
            api = TwitterAPI(self.TW_CONSUMER_KEY, self.TW_CONSUMER_SECRET, self.TW_TOKEN, self.TW_TOKEN_SECRET)
            tracks_data = { 'track' : "{0}".format( ",".join(self.track_text ) ) }

            stream_res = api.request('statuses/filter', tracks_data).get_iterator()
            for item in stream_res:
                # omit retweets
                if 'retweeted_status' in item:
                    continue

                if 'text' in item:
                    self.pool.spawn(self.redis_pub, item)
                    gevent.sleep(1)
        except Exception as e:
            self.error_print(e)


    # redis publish method
    # def redis_pub(self, tweet):
    #     try:
    #         for t_t in self.track_text:
    #             if t_t in tweet['text']:
    #                 # pprint( 'redis published, twitter id is %s'%(tweet['id_str']) )
    #                 self.redis_conn.publish(t_t, json.dumps(tweet))
    #     except Exception as e:
    #         self.error_print(e)
    
    def redis_pub(self, tweet):
        try:
            published = False

            if not published:
                for mention in tweet['entities']['user_mentions']:
                    if '@'+mention['screen_name'] in self.track_text:
                        published = True
                        self.redis_conn.publish('@'+mention['screen_name'], json.dumps(tweet))

            if not published:
                for hashtag in tweet['entities']['hashtags']:
                    if '#'+hashtag['text'] in self.track_text:
                        self.redis_conn.publish('#'+hashtag['text'], json.dumps(tweet))
        except Exception as e:
            self.error_print(e)


    # get all twitter tracks data
    def get_tw_tracks(self):
        try:
            db = self.connect_db_mysql()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            query = ('''SELECT * FROM twitter_tracks order by id desc''')
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            db.close()

            tracks_data = []
            if rows:
                for t_d in rows:
                    tracks_data.append(t_d['text'])

            return tracks_data
        except Exception as e:
            self.error_print(e)


    # get the last twitter track id
    def get_tw_last_track_id(self):
        try:
            db = self.connect_db_mysql()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            query = ('''SELECT id FROM twitter_tracks order by id desc limit 1''')
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
# get all twitter tracks data
tw_tracks_data = stream.get_tw_tracks()
latest_track_id = stream.get_tw_last_track_id()

# start running streaming
streaming_stopped = True
while True:
    try:
        # get the last insert track id
        last_insert_track_id = stream.get_tw_last_track_id()

        # check streaming is running or not
        if streaming_stopped:
            # running thread
            thread_m = gevent.spawn(stream.twitter_track, tw_tracks_data)

            # if thread start, set stop variable to false
            streaming_stopped = not thread_m.started

        # if last insert track id is changed
        if last_insert_track_id != latest_track_id:
            # kill thread and get new track data
            thread_m.kill()
            streaming_stopped = True
            tw_tracks_data = stream.get_tw_tracks()
            latest_track_id = last_insert_track_id


        gevent.sleep(10)
    except Exception as e:
        print(e)
