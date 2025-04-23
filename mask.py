import requests
import json

url = "https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json"
response = requests.get(url)
data = response.json()

# 取出 features 並轉成 list
pharmacy_list = data.get('features', [])

# 測試印出前 1 筆資料
# print(pharmacy_list[:1])

# 依據county欄位進行分組，計算每個county 口罩數量，區分大人跟小孩的剩餘數量
pharmacy_county = {}
for pharmacy in pharmacy_list:
    properties = pharmacy.get('properties', {})
    county = properties.get('county', '')
    if not county:
        address = properties.get('address', '')
        county = address[:3] if len(address) >= 3 else address
    mask_adult = properties.get('mask_adult', 0)
    mask_child = properties.get('mask_child', 0)

    if county not in pharmacy_county:
        pharmacy_county[county] = {'mask_adult': 0, 'mask_child': 0}

    pharmacy_county[county]['mask_adult'] += mask_adult
    pharmacy_county[county]['mask_child'] += mask_child
    

# 列印所有county的口罩數量
for county, masks in pharmacy_county.items():
    print(f"County: {county}, Adult Masks: {masks['mask_adult']}, Child Masks: {masks['mask_child']}")