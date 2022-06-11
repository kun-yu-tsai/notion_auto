from zoneinfo import ZoneInfo
from datetime import datetime

d = datetime.fromisoformat('2012-11-01T04:16:13.000Z')
print(d)

utc = datetime.utcnow()
now = datetime.now()

print(utc)
print(now)

print(utc.isoformat())
print(now.isoformat())

utc = utc.replace(tzinfo=ZoneInfo('UTC'))
# print(utc)
# utc = utc.replace(tzinfo=ZoneInfo('Asia/Taipei'))
print(utc)
tp_time = utc.astimezone(ZoneInfo("Asia/Taipei"))
print(tp_time)

# database_time = datetime.utcnow()
# print(database_time)

# database_time.replace(tzinfo=ZoneInfo('UTC'))
# d = database_time.astimezone(ZoneInfo("Europe/Berlin"))
# d2 = database_time.astimezone(ZoneInfo("Asia/Taipei"))
# print(d)
# print(d2)


# utc_unaware = datetime(2020, 10, 31, 12)  # loaded from database
# utc_aware = utc_unaware.replace(tzinfo=ZoneInfo('UTC'))  # make aware
# local_aware = utc_aware.astimezone(ZoneInfo("Asia/Taipei"))

# print(utc_unaware)
# print(utc_aware)
# print(local_aware)