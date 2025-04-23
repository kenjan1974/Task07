import requests
import json
import sqlite3
from datetime import datetime

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

# 建立 SQLite 連線與資料表
conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()

# 建立藥局數量資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS pharmacy_count (
    county TEXT PRIMARY KEY,
    count INTEGER,
    updated_at TEXT
)
''')

# 建立口罩剩餘數量資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS mask_remain (
    county TEXT PRIMARY KEY,
    mask_adult INTEGER,
    mask_child INTEGER,
    updated_at TEXT
)
''')

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 儲存藥局數量到資料庫
for county, count in pharmacy_county_count.items():
    cursor.execute('''
    INSERT OR REPLACE INTO pharmacy_count (county, count, updated_at)
    VALUES (?, ?, ?)
    ''', (county, count, now))

# 儲存口罩剩餘數量到資料庫
for county, masks in pharmacy_county_masks.items():
    cursor.execute('''
    INSERT OR REPLACE INTO mask_remain (county, mask_adult, mask_child, updated_at)
    VALUES (?, ?, ?, ?)
    ''', (county, masks['mask_adult'], masks['mask_child'], now))

conn.commit()
conn.close()

# 從資料庫取出各地區口罩數量，並先在資料庫依據成人口罩數量排序(降冪)
conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()
cursor.execute('''
SELECT county, mask_adult, mask_child FROM mask_remain ORDER BY mask_adult DESC
''')
rows = cursor.fetchall()    
conn.close()

# 列印從資料庫取出的各地區口罩數量
print("\n從資料庫取出的各地區口罩數量:")
for row in rows:
    county, mask_adult, mask_child = row
    print(f"County: {county}, Adult Masks: {mask_adult}, Child Masks: {mask_child}")



    



