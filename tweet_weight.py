import twitter
from twitter.error import TwitterError
import psycopg2
import os
from datetime import date
import argparse 

def check_date_isoformat(str_date):
  #todo
  return True 

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", type=str, help="User ID")
    parser.add_argument("date", type=str, help="Date ex: 2020-01-01") 
    args = parser.parse_args()

    user_id = args.user_id
    dt = args.date

    if not check_date_isoformat(dt):
        raise Exception(dt + " is not isoformat")
   
    twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY'] 
    twitter_consumer_secret = os.environ['TWITTER_CONSUMER_SECRET'] 
    twitter_access_token_key = os.environ['TWITTER_ACCESS_TOKEN_KEY'] 
    twitter_access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET'] 
    
    pg_dbname = os.environ['PG_WEIGHTER_DBNAME'] 
    pg_user = os.environ['PG_WEIGHTER_USER'] 
    pg_host = os.environ['PG_WEIGHTER_HOST'] 
    pg_password = os.environ['PG_WEIGHTER_PASSWORD'] 

    conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(pg_dbname, pg_user, pg_host, pg_password))
    cur = conn.cursor()    
    cur.execute("select weight from weight_data where id = %s and to_char(insert_date, 'YYYY-MM-dd') = %s;", (user_id, dt))
    row = cur.fetchone()
    if row is None:
        raise Exception('体重データが取得できませんでした。')

    weight = row[0]
 
    api = twitter.Api(consumer_key=twitter_consumer_key,
                    consumer_secret=twitter_consumer_secret,
                    access_token_key=twitter_access_token_key,
                    access_token_secret=twitter_access_token_secret)

    status = api.PostUpdates('{0} :{1}Kg'.format(dt, weight))
  
except KeyError as e:
    print('KeyError')
    print(e)
    exit(1)

except TwitterError as e:
    print('TwitterError')
    print(e)
    exit(1)

except Exception as e:
    print('Exception')
    print(e)
    exit(1)

print('Success to tweet!!')
print(status)
