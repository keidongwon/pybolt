from datetime import timezone, datetime
import pytz


def utc_to_local(utc_dt, local_tz=None):
	if type(utc_dt) == str:
		utc_dt = datetime.strptime(utc_dt, '%Y-%m-%d %H:%M:%S')
	local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
	return local_dt.strftime('%Y-%m-%d %H:%M:%S')
