import requests
import json

url = "https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json"
response = requests.get(url)
data = response.json()

# 取出 features 並轉成 list
pharmacy_list = data.get('features', [])

# 測試印出前 1 筆資料
print(pharmacy_list[:1])
