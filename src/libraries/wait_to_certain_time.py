from libraries.docker_log import log_info
from datetime import datetime, timedelta
import time

def absolute_next_round_minute():
    now = datetime.now()
    next_round_minute = now - timedelta(minutes=now.minute % 10,
                                        seconds=now.second,
                                        microseconds=now.microsecond)
    next_round_minute = next_round_minute + timedelta(minutes=10)
    return next_round_minute

def wait_minutes_after_round_minute(minutes):
    delta = timedelta(minutes=minutes)
    next_round_minute_time = absolute_next_round_minute()
    next_moment = (next_round_minute_time + delta)
    now = datetime.now()
    wait_seconds = (next_moment - now).seconds
    log_info("Waiting " + str(wait_seconds) + " seconds to start in " + str(next_moment))
    time.sleep(wait_seconds)



