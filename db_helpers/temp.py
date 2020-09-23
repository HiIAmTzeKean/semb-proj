import datetime


d = datetime.datetime.today()
d2 = datetime.datetime.strptime('2020/9/30', '%Y/%m/%d')
print(d + datetime.timedelta(days=20))
print(d2)
print(abs(d2-d).days)