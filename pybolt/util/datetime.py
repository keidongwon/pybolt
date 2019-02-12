from datetime import timezone, datetime


def utc_to_local(utc_dt):
	if type(utc_dt) == str:
		utc_dt = datetime.strptime(utc_dt, '%Y-%m-%d %H:%M:%S')
	local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
	return local_dt.strftime('%Y-%m-%d %H:%M:%S')
