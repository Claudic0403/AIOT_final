import requests
import json
import numpy as np
from datetime import datetime, time
import mysql.connector

DIST = {
  "外埔區":0,
  "新社區":1,
  "豐原區":2,
  "后里區":3,
  "北區":4,
  "太平區":5,
  "潭子區":6,
  "南屯區":7,
  "和平區":8,
  "大甲區":9,
  "中區":10,
  "烏日區":11,
  "沙鹿區":12,
  "南區":13,
  "龍井區":14,
  "石岡區":15,
  "東勢區":16,
  "北屯區":17,
  "西區":18,
  "霧峰區":19,
  "神岡區":20,
  "西屯區":21,
  "大里區":22,
  "大雅區":23,
  "大安區":24,
  "清水區":25,
  "東區":26,
  "大肚區":27,
  "梧棲區":28,
}

element_wea = {
  "PoP12h":0,
  "T":1,
  "RH":2,
  "MinCI":3,
  "WS":4,
  "MaxAT":5,
  "Wx":6,
  "MaxCI":7,
  "MinT":8,
  "UVI":9,
  "WeatherDescription":10,
  "MinAT":11,
  "MaxT":12,
  "WD":13,
  "Td":14,
}

Data = {
    'startTime' : [],
    'endTime' : [],
    'PoP12h' : [],
    'T' : [],
    'RH' : [],
    'MinCI' : [],
    'WS' : [],
    'MaxAT' : [],
    'Wx' : [],
    'MaxCI' : [],
    'MinT' : [],
    'UVI' : [],
    'WeatherDescription' : [],
    'MinAT' : [],
    'MaxT' : [],
    'WD' : [],
    'Td' : []
}

UVI = False
def get_data():
  for key in Data:
    Data[key] = []
  url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-075"
  params = {
      "Authorization": "CWB-FAFEF9F8-15ED-4671-B520-B85898EA133C", # 請改成自己的 API 授權碼
  }

  response = requests.get(url, params=params)
  # print(response.status_code)

  if response.status_code == 200:
    # print(response.text)
    data = json.loads(response.text)

    district = '南區'
    weather_elements = data["records"]['locations'][0]['location'][DIST[district]]["weatherElement"]
    LEN = len(weather_elements[0]['time'])
    
    current_time = datetime.now().time()
    # print(current_time)
    if current_time < time(6, 0, 0) or current_time > time(18, 0, 0):
      UVI = False
    else:
      UVI = True
    for i in range(LEN):
      for key in Data:
        if key == 'PoP12h' and i > 5:
          Data[key].append("NULL")
        elif key == 'UVI':
          if UVI:
            if not i%2 :
              Data[key].append(weather_elements[element_wea[key]]['time'][i//2]['elementValue'][0]['value'])
            else:
              Data[key].append("NULL")
          else:
            if i%2 :
              Data[key].append(weather_elements[element_wea[key]]['time'][i//2]['elementValue'][0]['value'])
            else:
              Data[key].append("NULL")
        elif key == 'startTime':
          Data[key].append(weather_elements[0]['time'][i]['startTime'])
        elif key == 'endTime':
          Data[key].append(weather_elements[0]['time'][i]['endTime'])
        else:
          Data[key].append(weather_elements[element_wea[key]]['time'][i]['elementValue'][0]['value'])
  else:
    print("Can't get data!")

def print_data(Data):
  LEN = len(Data.get('startTime'))
  # print(LEN)
  for i in range(LEN):
    for key in Data:
      if key == 'startTime':
        print("")
      elif key == 'endTime':
        print("From {} to {}".format(Data['startTime'][i], Data['endTime'][i]))
      elif key == 'UVI':
        if UVI:
          if not i%2:
            print("UVI : {}".format(Data['UVI'][i]))
          else:
            print("UVI : NULL")
        else:
          if i%2:
            print("UVI : {}".format(Data['UVI'][i]))
          else:
            print("UVI : NULL")
      else:
        print("{} : {}".format(key, Data[key][i]))

if __name__ == '__main__':
  get_data()
  print_data()
#   cnx = mysql.connector.connect(
#     host='172.20.10.4',
#     user='4109064206',
#     password='4109064206',
#     database='aiotdb'
#   )
#   c = cnx.cursor()

# LEN = len(Data['endTime'])
# for i in range(LEN):
#   c.execute("""INSERT INTO project_table (signalType, startTime, endTime, PoP12h, T, RH, MinCI, WS, MaxAT, Wx, MaxCI, MinT, UVI, WeatherDescription, MinAT, MaxT, WD, Td)\
#         VALUES ('%s', '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, '%s', %s, %s, '%s', %s, %s)""",\
#         ('d', Data["startTime"][i], Data["endTime"][i], Data["PoP12h"][i], Data["T"][i], Data["RH"][i], Data["MinCI"][i], Data["WS"][i], Data["MaxAT"][i], \
#         Data["Wx"][i], Data["MaxCI"][i], Data["MinT"][i], Data["UVI"][i], Data["WeatherDescription"][i], Data["MinAT"][i], Data["MaxT"][i], Data["WD"][i], Data["Td"][i]))
#   c.commit()

# c.close()
