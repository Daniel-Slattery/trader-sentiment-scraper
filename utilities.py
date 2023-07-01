from datetime import datetime
from pytz import timezone

def is_forex_market_open():
    now_est = datetime.now(timezone('US/Eastern'))
    open_time_sunday = datetime.strptime('16:00:00', '%H:%M:%S').time()
    close_time_friday = datetime.strptime('17:00:00', '%H:%M:%S').time()

    # If it's currently the weekend
    if now_est.weekday() > 4:
        if now_est.weekday() == 6:  # if it's Sunday
            if now_est.time() > open_time_sunday:
                return True
            else:
                return False
        else:  # if it's Saturday
            return False
    else:  # if it's a weekday
        if now_est.weekday() == 4:  # if it's Friday
            if now_est.time() > close_time_friday:
                return False
            else:
                return True
        else:  # if it's Monday-Thursday
            return True
