import requests
import json

url = "https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json"
response = requests.get(url)
data = response.json()

# 取出 features 並轉成 list
pharmacy_list = data.get('features', [])

# 測試印出前 1 筆資料
# print(pharmacy_list[:1])

def get_county(properties):
    county = properties.get('county', '')
    if not county:
        address = properties.get('address', '')
        county = address[:3] if len(address) >= 3 else address
    return county

pharmacy_county_count = {}
pharmacy_county_masks = {}
for pharmacy in pharmacy_list:
    properties = pharmacy.get('properties', {})
    county = get_county(properties)
    # 藥局數量統計
    if county not in pharmacy_county_count:
        pharmacy_county_count[county] = 0
    pharmacy_county_count[county] += 1
    # 口罩數量統計
    mask_adult = properties.get('mask_adult', 0)
    mask_child = properties.get('mask_child', 0)
    if county not in pharmacy_county_masks:
        pharmacy_county_masks[county] = {'mask_adult': 0, 'mask_child': 0}
    pharmacy_county_masks[county]['mask_adult'] += mask_adult
    pharmacy_county_masks[county]['mask_child'] += mask_child

# 列印出各county藥局數量
print("各county藥局數量:")
for county, count in pharmacy_county_count.items():
    print(f"County: {county}, Pharmacy Count: {count}")

# 依據成人口罩數量排序
pharmacy_county_masks = dict(sorted(pharmacy_county_masks.items(), key=lambda item: item[1]['mask_adult'], reverse=True))

# 列印所有county的口罩數量
print("\n各county口罩數量:")
for county, masks in pharmacy_county_masks.items():
    print(f"County: {county}, Adult Masks: {masks['mask_adult']}, Child Masks: {masks['mask_child']}")
    
    