#!/usr/bin/env python3
import redis
import time
import sys


def main():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    ps = r.pubsub()

    print("dsl_log: door_event log started")
    sys.stdout.flush()

    try:
        ps.subscribe('door_event')
        for m in ps.listen():
            if not m:
                print("event None received")
            elif m['type'] == 'subscribe':
                print("subscribe channel={}".format(m['channel']))
            elif m['type'] != 'message':
                print("event {}".format(m))
            else:
                print("message {} {}".format(time.time(), m['data']))

            sys.stdout.flush()

            #if not m or m['type'] != 'message':
            #    print("ignored message")
            #
            #m = json.loads(m['data'])
            #print("time={} event={} user_id={}".format(time.time(), m['event'], m['user_id']))

    finally:
        ps.unsubscribe()


if __name__ == '__main__':
    main()
