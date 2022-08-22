from datetime import date, datetime
import os
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import random
import json

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']


app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://www.yiketianqi.com/free/day?appid=98698738&appsecret=HBaaB40E&unescape=1&city=" + city
  res = requests.get(url).json()
  s1 = json.dumps(res)
  res = json.loads(s1)
  return res['wea'], res['tem'],res['tem_night'],res['tem_day']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthdayboy():
  next = datetime.strptime(str(date.today().year) + "-" + '03-11', "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_remembrance():
 next = datetime.strptime(str(date.today().year) + "-" + '08-19', "%Y-%m-%d")
 if next < datetime.now():
  next = next.replace(year=next.year + 1)
 return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea1, temperature, min_temp, max_temp = get_weather()
data = {"weather":{"value":wea1},"temperature":{"value":temperature},"min_temperature":{"value":min_temp},"max_temperature":{"value":max_temp},"love_days":{"value":get_count()},"birthday":{"value":get_birthday()},"birthdayboy":{"value":get_birthdayboy()},"remembranceday":{"value":get_remembrance()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
